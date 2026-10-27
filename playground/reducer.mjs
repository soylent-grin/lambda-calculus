const DEFS = [
  ["TRUE", "\\t. \\f. t"],
  ["FALSE", "\\t. \\f. f"],
  ["IF", "\\c. \\t. \\f. c t f"],
  ["NOT", "\\b. \\t. \\f. b f t"],
  ["AND", "\\a. \\b. a b FALSE"],
  ["OR", "\\a. \\b. a TRUE b"],
  ["ZERO", "\\f. \\x. x"],
  ["ONE", "\\f. \\x. f x"],
  ["TWO", "\\f. \\x. f (f x)"],
  ["THREE", "\\f. \\x. f (f (f x))"],
  ["SUCC", "\\n. \\f. \\x. f (n f x)"],
  ["ADD", "\\m. \\n. m SUCC n"],
  ["MUL", "\\m. \\n. \\f. m (n f)"],
  ["ISZERO", "\\n. n (\\x. FALSE) TRUE"],
  ["PRED", "\\n. \\f. \\x. n (\\g. \\h. h (g f)) (\\u. x) (\\u. u)"],
  ["PAIR", "\\a. \\b. \\s. s a b"],
  ["FST", "\\p. p TRUE"],
  ["SND", "\\p. p FALSE"],
  ["NIL", "\\c. \\n. n"],
  ["CONS", "\\h. \\t. \\c. \\n. c h (t c n)"],
  ["I", "\\x. x"],
  ["K", "\\x. \\y. x"],
  ["S", "\\x. \\y. \\z. x z (y z)"],
  ["Y", "\\f. (\\x. f (x x)) (\\x. f (x x))"],
  ["Z", "\\f. (\\x. f (\\y. x x y)) (\\x. f (\\y. x x y))"],
  ["Ω", "(\\x. x x) (\\x. x x)"],
  ["FACT", "Y (\\self. \\n. IF (ISZERO n) ONE (MUL n (self (PRED n))))"],
];

function clone(term) {
  if (term.tag === "var") return { tag: "var", name: term.name };
  if (term.tag === "macro") return { tag: "macro", name: term.name, term: clone(term.term) };
  if (term.tag === "lam") return { tag: "lam", param: term.param, body: clone(term.body) };
  return { tag: "app", fn: clone(term.fn), arg: clone(term.arg) };
}

function walk(term) {
  let guard = 0;
  while (term.tag === "macro" && guard++ < 32) term = term.term;
  return term;
}

function freeIn(term, name) {
  const node = walk(term);
  if (node.tag === "var") return node.name === name;
  if (node.tag === "lam") return node.param !== name && freeIn(node.body, name);
  if (node.tag === "app") return freeIn(node.fn, name) || freeIn(node.arg, name);
  return false;
}

function usedNames(term, acc = new Set()) {
  const node = walk(term);
  if (node.tag === "var") acc.add(node.name);
  else if (node.tag === "lam") {
    acc.add(node.param);
    usedNames(node.body, acc);
  } else if (node.tag === "app") {
    usedNames(node.fn, acc);
    usedNames(node.arg, acc);
  }
  return acc;
}

function fresh(base, used) {
  let i = 1;
  let name = `${base}${i}`;
  while (used.has(name)) {
    i += 1;
    name = `${base}${i}`;
  }
  return name;
}

function subst(term, name, value) {
  if (term.tag === "macro") return clone(term);
  if (term.tag === "var") return term.name === name ? clone(value) : clone(term);
  if (term.tag === "lam") {
    if (term.param === name) return clone(term);
    if (freeIn(value, term.param)) {
      const used = usedNames(term.body);
      usedNames(value, used);
      used.add(name);
      const param = fresh(term.param, used);
      const renamed = subst(term.body, term.param, { tag: "var", name: param });
      return { tag: "lam", param, body: subst(renamed, name, value) };
    }
    return { tag: "lam", param: term.param, body: subst(term.body, name, value) };
  }
  return { tag: "app", fn: subst(term.fn, name, value), arg: subst(term.arg, name, value) };
}

function findRedex(term, mode) {
  const node = walk(term);
  if (node.tag === "lam") return findRedex(node.body, mode);
  if (node.tag !== "app") return null;
  if (mode === "name") {
    if (walk(node.fn).tag === "lam") return node;
    return findRedex(node.fn, mode) || findRedex(node.arg, mode);
  }
  return (
    findRedex(node.fn, mode) ||
    findRedex(node.arg, mode) ||
    (walk(node.fn).tag === "lam" ? node : null)
  );
}

function contract(redex) {
  const fn = walk(redex.fn);
  return subst(fn.body, fn.param, redex.arg);
}

function contains(term, target) {
  if (!target) return false;
  if (term === target) return true;
  if (term.tag === "macro") return contains(term.term, target);
  if (term.tag === "lam") return contains(term.body, target);
  if (term.tag === "app") return contains(term.fn, target) || contains(term.arg, target);
  return false;
}

function replace(term, target, next) {
  if (term === target) return next;
  if (term.tag === "macro") {
    const inner = replace(term.term, target, next);
    return inner === term.term ? term : inner;
  }
  if (term.tag === "lam") {
    const body = replace(term.body, target, next);
    return body === term.body ? term : { tag: "lam", param: term.param, body };
  }
  if (term.tag === "app") {
    const fn = replace(term.fn, target, next);
    const arg = replace(term.arg, target, next);
    return fn === term.fn && arg === term.arg ? term : { tag: "app", fn, arg };
  }
  return term;
}

function step(term, mode) {
  const redex = findRedex(term, mode);
  if (!redex) return null;
  const next = contract(redex);
  if (walk(term) === redex) return next;
  return replace(term, redex, next);
}

function escapeHtml(text) {
  return text.replaceAll("&", "&amp;").replaceAll("<", "&lt;").replaceAll(">", "&gt;");
}

function pretty(term, redex) {
  const node = term;
  let text;
  if (node.tag === "macro") {
    text = escapeHtml(node.name);
    if (contains(node, redex)) return `<span class="redex">${text}</span>`;
    return text;
  }
  else if (node.tag === "var") text = escapeHtml(node.name);
  else if (node.tag === "lam") text = `λ${escapeHtml(node.param)}. ${pretty(node.body, redex)}`;
  else {
    const fn = walk(node.fn).tag === "lam" ? `(${pretty(node.fn, redex)})` : pretty(node.fn, redex);
    const arg = node.arg.tag === "var" || node.arg.tag === "macro" ? pretty(node.arg, redex) : `(${pretty(node.arg, redex)})`;
    text = `${fn} ${arg}`;
  }
  if (node === redex) return `<span class="redex">${text}</span>`;
  return text;
}

function plain(term) {
  return pretty(term, null).replaceAll(/<[^>]+>/g, "");
}

class ParseError extends Error {}

function tokenize(input) {
  const source = input.replaceAll("λ", "\\");
  const tokens = [];
  let i = 0;
  while (i < source.length) {
    const ch = source[i];
    if (/\s/.test(ch)) {
      i += 1;
      continue;
    }
    if ("\\.()".includes(ch)) {
      tokens.push({ type: ch, at: i });
      i += 1;
      continue;
    }
    if (ch === "Ω" || /[A-Za-z_]/.test(ch)) {
      const start = i;
      i += 1;
      while (i < source.length && /[A-Za-z0-9_]/.test(source[i])) i += 1;
      tokens.push({ type: "id", value: source.slice(start, i), at: start });
      continue;
    }
    throw new ParseError(`неизвестный символ «${ch}»`);
  }
  return tokens;
}

function parse(input, env) {
  const tokens = tokenize(input);
  let i = 0;
  const peek = () => tokens[i];
  const eat = (type) => {
    const token = tokens[i];
    if (!token || token.type !== type) {
      throw new ParseError(type === "id" ? "ожидалось имя" : `ожидалось «${type === "\\" ? "λ" : type}»`);
    }
    i += 1;
    return token;
  };
  const parseAtom = (bound) => {
    const token = peek();
    if (!token) throw new ParseError("терм обрывается");
    if (token.type === "(") {
      eat("(");
      const inner = parseTerm(bound);
      eat(")");
      return inner;
    }
    if (token.type === "\\") return parseLam(bound);
    if (token.type === "id") {
      eat("id");
      if (!bound.has(token.value) && env[token.value]) return clone(env[token.value]);
      return { tag: "var", name: token.value };
    }
    throw new ParseError("ожидался терм");
  };
  const parseLam = (bound) => {
    eat("\\");
    const name = eat("id").value;
    eat(".");
    const next = new Set(bound);
    next.add(name);
    return { tag: "lam", param: name, body: parseTerm(next) };
  };
  const startsAtom = (token) => token && (token.type === "id" || token.type === "\\" || token.type === "(");
  const parseTerm = (bound) => {
    if (peek()?.type === "\\" && tokens[i + 1]?.type === "id" && tokens[i + 2]?.type === ".") {
      return parseLam(bound);
    }
    let left = parseAtom(bound);
    while (startsAtom(peek())) left = { tag: "app", fn: left, arg: parseAtom(bound) };
    return left;
  };
  if (tokens.length === 0) throw new ParseError("пустой терм");
  const term = parseTerm(new Set());
  if (i < tokens.length) throw new ParseError("после терма остались лишние символы");
  return term;
}

function buildEnv() {
  const env = {};
  for (const [name, source] of DEFS) {
    env[name] = { tag: "macro", name, term: parse(source, env) };
  }
  return env;
}

const ENV = buildEnv();

function alphaEq(a, b) {
  function go(x, y, env, rightBound) {
    x = walk(x);
    y = walk(y);
    if (x.tag !== y.tag) return false;
    if (x.tag === "var") {
      if (env.has(x.name)) return env.get(x.name) === y.name;
      return x.name === y.name && !rightBound.has(y.name);
    }
    if (x.tag === "lam") {
      const next = new Map(env);
      next.set(x.param, y.param);
      const bound = new Set(rightBound);
      bound.add(y.param);
      return go(x.body, y.body, next, bound);
    }
    return go(x.fn, y.fn, env, rightBound) && go(x.arg, y.arg, env, rightBound);
  }
  return go(a, b, new Map(), new Set());
}

function churchNumber(term) {
  const outer = walk(term);
  if (outer.tag !== "lam") return null;
  const inner = walk(outer.body);
  if (inner.tag !== "lam" || inner.param === outer.param) return null;
  let node = walk(inner.body);
  let count = 0;
  while (node.tag === "app") {
    const fn = walk(node.fn);
    if (fn.tag !== "var" || fn.name !== outer.param) return null;
    count += 1;
    node = walk(node.arg);
  }
  return node.tag === "var" && node.name === inner.param ? count : null;
}

// names the value of a normal form when it matches a known encoding
function decode(term) {
  if (alphaEq(term, ENV.TRUE)) return "TRUE";
  if (alphaEq(term, ENV.FALSE)) return "FALSE · или число 0";
  const n = churchNumber(term);
  if (n !== null) return n === 1 ? "число 1 · или I" : `число ${n}`;
  if (alphaEq(term, ENV.I)) return "I, тождественная функция";
  return null;
}

const DEFINITIONS = DEFS.map(([name, source]) => [name, source.replaceAll("\\", "λ")]);

export { DEFINITIONS, ENV, alphaEq, decode, findRedex, parse, plain, pretty, step };
