import assert from "node:assert/strict";
import test from "node:test";
import { ENV, alphaEq, decode, parse, plain, step } from "./reducer.mjs";

function norm(source, mode = "name", fuel = 80) {
  let term = parse(source, ENV);
  const seen = new Set();
  for (let i = 0; i < fuel; i += 1) {
    const key = plain(term);
    if (seen.has(key)) return { term, diverges: true, steps: i };
    seen.add(key);
    const next = step(term, mode);
    if (!next) return { term, diverges: false, steps: i };
    term = next;
  }
  return { term, diverges: true, steps: fuel };
}

test("identity", () => {
  const once = step(parse("(\\x. x) y", ENV), "name");
  assert.equal(plain(once), "y");
});

test("capture is avoided", () => {
  const once = step(parse("(\\x. \\y. x) y", ENV), "name");
  assert.equal(plain(once), "λy1. y");
  assert.notEqual(plain(once), "λy. y");
});

test("booleans and pairs", () => {
  assert.equal(plain(norm("IF TRUE a b").term), "a");
  assert.equal(plain(norm("IF FALSE a b").term), "b");
  assert.ok(alphaEq(norm("NOT TRUE").term, ENV.FALSE));
  assert.ok(alphaEq(norm("NOT FALSE").term, ENV.TRUE));
  assert.ok(alphaEq(norm("AND TRUE FALSE").term, ENV.FALSE));
  assert.ok(alphaEq(norm("AND TRUE TRUE").term, ENV.TRUE));
  assert.equal(plain(norm("FST (PAIR a b)").term), "a");
  assert.equal(plain(norm("SND (PAIR a b)").term), "b");
});

test("arithmetic", () => {
  assert.ok(alphaEq(norm("SUCC ONE").term, ENV.TWO));
  assert.ok(alphaEq(norm("ADD ONE ONE").term, ENV.TWO));
  assert.ok(alphaEq(norm("ADD TWO ONE").term, ENV.THREE));
  assert.ok(alphaEq(norm("MUL TWO TWO").term, parse("\\f. \\x. f (f (f (f x)))", ENV)));
});

test("omega and strategies", () => {
  const loop = norm("Ω", "name", 6);
  assert.equal(loop.diverges, true);
  const lazy = norm("(\\x. \\y. y) Ω", "name", 10);
  assert.equal(lazy.diverges, false);
  assert.ok(alphaEq(lazy.term, parse("\\y. y", ENV)));
  const eager = norm("(\\x. \\y. y) Ω", "value", 8);
  assert.equal(eager.diverges, true);
  const eagerOnce = step(parse("(\\x. \\y. y) Ω", ENV), "value");
  assert.match(plain(eagerOnce), /\(λx\. x x\) \(λx\. x x\)/);
});

test("lesson results", () => {
  const value = (src, mode = "name", fuel = 1000) => decode(norm(src, mode, fuel).term);
  assert.equal(plain(norm("(λx. λy. x) a").term), "λy. a");
  assert.equal(plain(norm("(λf. λx. f (f x)) g a").term), "g (g a)");
  assert.equal(plain(norm("TRUE a b").term), "a");
  assert.equal(plain(norm("IF FALSE yes no").term), "no");
  assert.equal(value("AND TRUE (NOT FALSE)"), "TRUE");
  assert.equal(plain(norm("THREE g a").term), "g (g (g a))");
  assert.equal(value("SUCC TWO"), "число 3");
  assert.equal(value("ADD TWO THREE"), "число 5");
  assert.equal(value("MUL TWO THREE"), "число 6");
  assert.equal(value("ISZERO (PRED ONE)"), "TRUE");
  assert.equal(value("PRED THREE"), "число 2");
  assert.equal(plain(norm("SND (PAIR a b)").term), "b");
  assert.equal(plain(norm("CONS a (CONS b NIL) f z").term), "f a (f b z)");
  assert.equal(value("CONS ONE (CONS TWO NIL) ADD ZERO"), "число 3");
  assert.equal(value("(λm. λn. n m) TWO THREE"), "число 8");
  assert.equal(plain(norm("S K S z").term), "z");
});

test("both orders agree when both finish", () => {
  const lazy = norm("(λx. g x x) ((λy. y) a)", "name");
  const eager = norm("(λx. g x x) ((λy. y) a)", "value");
  assert.equal(plain(lazy.term), "g a a");
  assert.equal(plain(eager.term), "g a a");
  assert.ok(lazy.steps > eager.steps);
});

test("factorial through Y", () => {
  assert.equal(decode(norm("FACT TWO", "name", 400).term), "число 2");
  assert.equal(decode(norm("FACT THREE", "name", 1200).term), "число 6");
});

test("ski and y", () => {
  assert.equal(plain(norm("S K K z").term), "z");
  const once = step(parse("Y g", ENV), "name");
  assert.equal(plain(once), "(λx. g (x x)) (λx. g (x x))");
});
