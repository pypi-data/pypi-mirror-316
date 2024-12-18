function e(e){var t,r,n=e.statementIndent,a=e.jsonld,i=e.json||a,o=e.typescript,u=e.wordCharacters||/[\w$\xa1-\uffff]/,c=function(){function e(e){return{type:e,style:"keyword"}}var t=e("keyword a"),r=e("keyword b"),n=e("keyword c"),a=e("keyword d"),i=e("operator"),o={type:"atom",style:"atom"};return{if:e("if"),while:t,with:t,else:r,do:r,try:r,finally:r,return:a,break:a,continue:a,new:e("new"),delete:n,void:n,throw:n,debugger:e("debugger"),var:e("var"),const:e("var"),let:e("var"),function:e("function"),catch:e("catch"),for:e("for"),switch:e("switch"),case:e("case"),default:e("default"),in:i,typeof:i,instanceof:i,true:o,false:o,null:o,undefined:o,NaN:o,Infinity:o,this:e("this"),class:e("class"),super:e("atom"),yield:n,export:e("export"),import:e("import"),extends:n,await:n}}(),s=/[+\-*&%=<>!?|~^@]/,l=/^@(context|id|value|language|type|container|list|set|reverse|index|base|vocab|graph)"/;function f(e,n,a){return t=e,r=a,n}function d(e,t){var r,n=e.next();if('"'==n||"'"==n)return t.tokenize=(r=n,function(e,t){var n,i=!1;if(a&&"@"==e.peek()&&e.match(l))return t.tokenize=d,f("jsonld-keyword","meta");for(;null!=(n=e.next())&&(n!=r||i);)i=!i&&"\\"==n;return i||(t.tokenize=d),f("string","string")}),t.tokenize(e,t);if("."==n&&e.match(/^\d[\d_]*(?:[eE][+\-]?[\d_]+)?/))return f("number","number");if("."==n&&e.match(".."))return f("spread","meta");if(/[\[\]{}\(\),;\:\.]/.test(n))return f(n);if("="==n&&e.eat(">"))return f("=>","operator");if("0"==n&&e.match(/^(?:x[\dA-Fa-f_]+|o[0-7_]+|b[01_]+)n?/))return f("number","number");if(/\d/.test(n))return e.match(/^[\d_]*(?:n|(?:\.[\d_]*)?(?:[eE][+\-]?[\d_]+)?)?/),f("number","number");if("/"==n)return e.eat("*")?(t.tokenize=m,m(e,t)):e.eat("/")?(e.skipToEnd(),f("comment","comment")):function(e,t,r){return t.tokenize==d&&/^(?:operator|sof|keyword [bcd]|case|new|export|default|spread|[\[{}\(,;:]|=>)$/.test(t.lastType)||"quasi"==t.lastType&&/\{\s*$/.test(e.string.slice(0,e.pos-r))}(e,t,1)?(function(e){for(var t,r=!1,n=!1;null!=(t=e.next());){if(!r){if("/"==t&&!n)return;"["==t?n=!0:n&&"]"==t&&(n=!1)}r=!r&&"\\"==t}}(e),e.match(/^\b(([gimyus])(?![gimyus]*\2))+\b/),f("regexp","string.special")):(e.eat("="),f("operator","operator",e.current()));if("`"==n)return t.tokenize=p,p(e,t);if("#"==n&&"!"==e.peek())return e.skipToEnd(),f("meta","meta");if("#"==n&&e.eatWhile(u))return f("variable","property");if("<"==n&&e.match("!--")||"-"==n&&e.match("->")&&!/\S/.test(e.string.slice(0,e.start)))return e.skipToEnd(),f("comment","comment");if(s.test(n))return">"==n&&t.lexical&&">"==t.lexical.type||(e.eat("=")?"!"!=n&&"="!=n||e.eat("="):/[<>*+\-|&?]/.test(n)&&(e.eat(n),">"==n&&e.eat(n))),"?"==n&&e.eat(".")?f("."):f("operator","operator",e.current());if(u.test(n)){e.eatWhile(u);var i=e.current();if("."!=t.lastType){if(c.propertyIsEnumerable(i)){var o=c[i];return f(o.type,o.style,i)}if("async"==i&&e.match(/^(\s|\/\*([^*]|\*(?!\/))*?\*\/)*[\[\(\w]/,!1))return f("async","keyword",i)}return f("variable","variable",i)}}function m(e,t){for(var r,n=!1;r=e.next();){if("/"==r&&n){t.tokenize=d;break}n="*"==r}return f("comment","comment")}function p(e,t){for(var r,n=!1;null!=(r=e.next());){if(!n&&("`"==r||"$"==r&&e.eat("{"))){t.tokenize=d;break}n=!n&&"\\"==r}return f("quasi","string.special",e.current())}function k(e,t){t.fatArrowAt&&(t.fatArrowAt=null);var r=e.string.indexOf("=>",e.start);if(!(r<0)){if(o){var n=/:\s*(?:\w+(?:<[^>]*>|\[\])?|\{[^}]*\})\s*$/.exec(e.string.slice(e.start,r));n&&(r=n.index)}for(var a=0,i=!1,c=r-1;c>=0;--c){var s=e.string.charAt(c),l="([{}])".indexOf(s);if(l>=0&&l<3){if(!a){++c;break}if(0==--a){"("==s&&(i=!0);break}}else if(l>=3&&l<6)++a;else if(u.test(s))i=!0;else if(/["'\/`]/.test(s))for(;;--c){if(0==c)return;if(e.string.charAt(c-1)==s&&"\\"!=e.string.charAt(c-2)){c--;break}}else if(i&&!a){++c;break}}i&&!a&&(t.fatArrowAt=c)}}var v={atom:!0,number:!0,variable:!0,string:!0,regexp:!0,this:!0,import:!0,"jsonld-keyword":!0};function y(e,t,r,n,a,i){this.indented=e,this.column=t,this.type=r,this.prev=a,this.info=i,null!=n&&(this.align=n)}function w(e,t){for(var r=e.localVars;r;r=r.next)if(r.name==t)return!0;for(var n=e.context;n;n=n.prev)for(r=n.vars;r;r=r.next)if(r.name==t)return!0}var b={state:null,column:null,marked:null,cc:null};function h(){for(var e=arguments.length-1;e>=0;e--)b.cc.push(arguments[e])}function x(){return h.apply(null,arguments),!0}function g(e,t){for(var r=t;r;r=r.next)if(r.name==e)return!0;return!1}function V(t){var r=b.state;if(b.marked="def",r.context)if("var"==r.lexical.info&&r.context&&r.context.block){var n=A(t,r.context);if(null!=n)return void(r.context=n)}else if(!g(t,r.localVars))return void(r.localVars=new j(t,r.localVars));e.globalVars&&!g(t,r.globalVars)&&(r.globalVars=new j(t,r.globalVars))}function A(e,t){if(t){if(t.block){var r=A(e,t.prev);return r?r==t.prev?t:new T(r,t.vars,!0):null}return g(e,t.vars)?t:new T(t.prev,new j(e,t.vars),!1)}return null}function z(e){return"public"==e||"private"==e||"protected"==e||"abstract"==e||"readonly"==e}function T(e,t,r){this.prev=e,this.vars=t,this.block=r}function j(e,t){this.name=e,this.next=t}var $=new j("this",new j("arguments",null));function O(){b.state.context=new T(b.state.context,b.state.localVars,!1),b.state.localVars=$}function _(){b.state.context=new T(b.state.context,b.state.localVars,!0),b.state.localVars=null}function q(){b.state.localVars=b.state.context.vars,b.state.context=b.state.context.prev}function E(e,t){var r=function(){var r=b.state,n=r.indented;if("stat"==r.lexical.type)n=r.lexical.indented;else for(var a=r.lexical;a&&")"==a.type&&a.align;a=a.prev)n=a.indented;r.lexical=new y(n,b.stream.column(),e,null,r.lexical,t)};return r.lex=!0,r}function I(){var e=b.state;e.lexical.prev&&(")"==e.lexical.type&&(e.indented=e.lexical.indented),e.lexical=e.lexical.prev)}function S(e){return function t(r){return r==e?x():";"==e||"}"==r||")"==r||"]"==r?h():x(t)}}function N(e,t){return"var"==e?x(E("vardef",t),be,S(";"),I):"keyword a"==e?x(E("form"),B,N,I):"keyword b"==e?x(E("form"),N,I):"keyword d"==e?b.stream.match(/^\s*$/,!1)?x():x(E("stat"),F,S(";"),I):"debugger"==e?x(S(";")):"{"==e?x(E("}"),_,ne,I,q):";"==e?x():"if"==e?("else"==b.state.lexical.info&&b.state.cc[b.state.cc.length-1]==I&&b.state.cc.pop()(),x(E("form"),B,N,I,ze)):"function"==e?x(Oe):"for"==e?x(E("form"),_,Te,N,q,I):"class"==e||o&&"interface"==t?(b.marked="keyword",x(E("form","class"==e?e:t),Se,I)):"variable"==e?o&&"declare"==t?(b.marked="keyword",x(N)):o&&("module"==t||"enum"==t||"type"==t)&&b.stream.match(/^\s*\w/,!1)?(b.marked="keyword","enum"==t?x(Ke):"type"==t?x(qe,S("operator"),ce,S(";")):x(E("form"),he,S("{"),E("}"),ne,I,I)):o&&"namespace"==t?(b.marked="keyword",x(E("form"),C,N,I)):o&&"abstract"==t?(b.marked="keyword",x(N)):x(E("stat"),R):"switch"==e?x(E("form"),B,S("{"),E("}","switch"),_,ne,I,I,q):"case"==e?x(C,S(":")):"default"==e?x(S(":")):"catch"==e?x(E("form"),O,P,N,I,q):"export"==e?x(E("stat"),We,I):"import"==e?x(E("stat"),De,I):"async"==e?x(N):"@"==t?x(C,N):h(E("stat"),C,S(";"),I)}function P(e){if("("==e)return x(Ee,S(")"))}function C(e,t){return D(e,t,!1)}function W(e,t){return D(e,t,!0)}function B(e){return"("!=e?h():x(E(")"),F,S(")"),I)}function D(e,t,r){if(b.state.fatArrowAt==b.stream.start){var n=r?L:K;if("("==e)return x(O,E(")"),te(Ee,")"),I,S("=>"),n,q);if("variable"==e)return h(O,he,S("=>"),n,q)}var a=r?G:U;return v.hasOwnProperty(e)?x(a):"function"==e?x(Oe,a):"class"==e||o&&"interface"==t?(b.marked="keyword",x(E("form"),Ie,I)):"keyword c"==e||"async"==e?x(r?W:C):"("==e?x(E(")"),F,S(")"),I,a):"operator"==e||"spread"==e?x(r?W:C):"["==e?x(E("]"),Je,I,a):"{"==e?re(Y,"}",null,a):"quasi"==e?h(H,a):"new"==e?x(function(e){return function(t){return"."==t?x(e?Q:M):"variable"==t&&o?x(ve,e?G:U):h(e?W:C)}}(r)):x()}function F(e){return e.match(/[;\}\)\],]/)?h():h(C)}function U(e,t){return","==e?x(F):G(e,t,!1)}function G(e,t,r){var n=0==r?U:G,a=0==r?C:W;return"=>"==e?x(O,r?L:K,q):"operator"==e?/\+\+|--/.test(t)||o&&"!"==t?x(n):o&&"<"==t&&b.stream.match(/^([^<>]|<[^<>]*>)*>\s*\(/,!1)?x(E(">"),te(ce,">"),I,n):"?"==t?x(C,S(":"),a):x(a):"quasi"==e?h(H,n):";"!=e?"("==e?re(W,")","call",n):"."==e?x(X,n):"["==e?x(E("]"),F,S("]"),I,n):o&&"as"==t?(b.marked="keyword",x(ce,n)):"regexp"==e?(b.state.lastType=b.marked="operator",b.stream.backUp(b.stream.pos-b.stream.start-1),x(a)):void 0:void 0}function H(e,t){return"quasi"!=e?h():"${"!=t.slice(t.length-2)?x(H):x(F,J)}function J(e){if("}"==e)return b.marked="string.special",b.state.tokenize=p,x(H)}function K(e){return k(b.stream,b.state),h("{"==e?N:C)}function L(e){return k(b.stream,b.state),h("{"==e?N:W)}function M(e,t){if("target"==t)return b.marked="keyword",x(U)}function Q(e,t){if("target"==t)return b.marked="keyword",x(G)}function R(e){return":"==e?x(I,N):h(U,S(";"),I)}function X(e){if("variable"==e)return b.marked="property",x()}function Y(e,t){return"async"==e?(b.marked="property",x(Y)):"variable"==e||"keyword"==b.style?(b.marked="property","get"==t||"set"==t?x(Z):(o&&b.state.fatArrowAt==b.stream.start&&(r=b.stream.match(/^\s*:\s*/,!1))&&(b.state.fatArrowAt=b.stream.pos+r[0].length),x(ee))):"number"==e||"string"==e?(b.marked=a?"property":b.style+" property",x(ee)):"jsonld-keyword"==e?x(ee):o&&z(t)?(b.marked="keyword",x(Y)):"["==e?x(C,ae,S("]"),ee):"spread"==e?x(W,ee):"*"==t?(b.marked="keyword",x(Y)):":"==e?h(ee):void 0;var r}function Z(e){return"variable"!=e?h(ee):(b.marked="property",x(Oe))}function ee(e){return":"==e?x(W):"("==e?h(Oe):void 0}function te(e,t,r){function n(a,i){if(r?r.indexOf(a)>-1:","==a){var o=b.state.lexical;return"call"==o.info&&(o.pos=(o.pos||0)+1),x((function(r,n){return r==t||n==t?h():h(e)}),n)}return a==t||i==t?x():r&&r.indexOf(";")>-1?h(e):x(S(t))}return function(r,a){return r==t||a==t?x():h(e,n)}}function re(e,t,r){for(var n=3;n<arguments.length;n++)b.cc.push(arguments[n]);return x(E(t,r),te(e,t),I)}function ne(e){return"}"==e?x():h(N,ne)}function ae(e,t){if(o){if(":"==e)return x(ce);if("?"==t)return x(ae)}}function ie(e,t){if(o&&(":"==e||"in"==t))return x(ce)}function oe(e){if(o&&":"==e)return b.stream.match(/^\s*\w+\s+is\b/,!1)?x(C,ue,ce):x(ce)}function ue(e,t){if("is"==t)return b.marked="keyword",x()}function ce(e,t){return"keyof"==t||"typeof"==t||"infer"==t||"readonly"==t?(b.marked="keyword",x("typeof"==t?W:ce)):"variable"==e||"void"==t?(b.marked="type",x(ke)):"|"==t||"&"==t?x(ce):"string"==e||"number"==e||"atom"==e?x(ke):"["==e?x(E("]"),te(ce,"]",","),I,ke):"{"==e?x(E("}"),le,I,ke):"("==e?x(te(pe,")"),se,ke):"<"==e?x(te(ce,">"),ce):"quasi"==e?h(de,ke):void 0}function se(e){if("=>"==e)return x(ce)}function le(e){return e.match(/[\}\)\]]/)?x():","==e||";"==e?x(le):h(fe,le)}function fe(e,t){return"variable"==e||"keyword"==b.style?(b.marked="property",x(fe)):"?"==t||"number"==e||"string"==e?x(fe):":"==e?x(ce):"["==e?x(S("variable"),ie,S("]"),fe):"("==e?h(_e,fe):e.match(/[;\}\)\],]/)?void 0:x()}function de(e,t){return"quasi"!=e?h():"${"!=t.slice(t.length-2)?x(de):x(ce,me)}function me(e){if("}"==e)return b.marked="string.special",b.state.tokenize=p,x(de)}function pe(e,t){return"variable"==e&&b.stream.match(/^\s*[?:]/,!1)||"?"==t?x(pe):":"==e?x(ce):"spread"==e?x(pe):h(ce)}function ke(e,t){return"<"==t?x(E(">"),te(ce,">"),I,ke):"|"==t||"."==e||"&"==t?x(ce):"["==e?x(ce,S("]"),ke):"extends"==t||"implements"==t?(b.marked="keyword",x(ce)):"?"==t?x(ce,S(":"),ce):void 0}function ve(e,t){if("<"==t)return x(E(">"),te(ce,">"),I,ke)}function ye(){return h(ce,we)}function we(e,t){if("="==t)return x(ce)}function be(e,t){return"enum"==t?(b.marked="keyword",x(Ke)):h(he,ae,Ve,Ae)}function he(e,t){return o&&z(t)?(b.marked="keyword",x(he)):"variable"==e?(V(t),x()):"spread"==e?x(he):"["==e?re(ge,"]"):"{"==e?re(xe,"}"):void 0}function xe(e,t){return"variable"!=e||b.stream.match(/^\s*:/,!1)?("variable"==e&&(b.marked="property"),"spread"==e?x(he):"}"==e?h():"["==e?x(C,S("]"),S(":"),xe):x(S(":"),he,Ve)):(V(t),x(Ve))}function ge(){return h(he,Ve)}function Ve(e,t){if("="==t)return x(W)}function Ae(e){if(","==e)return x(be)}function ze(e,t){if("keyword b"==e&&"else"==t)return x(E("form","else"),N,I)}function Te(e,t){return"await"==t?x(Te):"("==e?x(E(")"),je,I):void 0}function je(e){return"var"==e?x(be,$e):"variable"==e?x($e):h($e)}function $e(e,t){return")"==e?x():";"==e?x($e):"in"==t||"of"==t?(b.marked="keyword",x(C,$e)):h(C,$e)}function Oe(e,t){return"*"==t?(b.marked="keyword",x(Oe)):"variable"==e?(V(t),x(Oe)):"("==e?x(O,E(")"),te(Ee,")"),I,oe,N,q):o&&"<"==t?x(E(">"),te(ye,">"),I,Oe):void 0}function _e(e,t){return"*"==t?(b.marked="keyword",x(_e)):"variable"==e?(V(t),x(_e)):"("==e?x(O,E(")"),te(Ee,")"),I,oe,q):o&&"<"==t?x(E(">"),te(ye,">"),I,_e):void 0}function qe(e,t){return"keyword"==e||"variable"==e?(b.marked="type",x(qe)):"<"==t?x(E(">"),te(ye,">"),I):void 0}function Ee(e,t){return"@"==t&&x(C,Ee),"spread"==e?x(Ee):o&&z(t)?(b.marked="keyword",x(Ee)):o&&"this"==e?x(ae,Ve):h(he,ae,Ve)}function Ie(e,t){return"variable"==e?Se(e,t):Ne(e,t)}function Se(e,t){if("variable"==e)return V(t),x(Ne)}function Ne(e,t){return"<"==t?x(E(">"),te(ye,">"),I,Ne):"extends"==t||"implements"==t||o&&","==e?("implements"==t&&(b.marked="keyword"),x(o?ce:C,Ne)):"{"==e?x(E("}"),Pe,I):void 0}function Pe(e,t){return"async"==e||"variable"==e&&("static"==t||"get"==t||"set"==t||o&&z(t))&&b.stream.match(/^\s+#?[\w$\xa1-\uffff]/,!1)?(b.marked="keyword",x(Pe)):"variable"==e||"keyword"==b.style?(b.marked="property",x(Ce,Pe)):"number"==e||"string"==e?x(Ce,Pe):"["==e?x(C,ae,S("]"),Ce,Pe):"*"==t?(b.marked="keyword",x(Pe)):o&&"("==e?h(_e,Pe):";"==e||","==e?x(Pe):"}"==e?x():"@"==t?x(C,Pe):void 0}function Ce(e,t){if("!"==t||"?"==t)return x(Ce);if(":"==e)return x(ce,Ve);if("="==t)return x(W);var r=b.state.lexical.prev;return h(r&&"interface"==r.info?_e:Oe)}function We(e,t){return"*"==t?(b.marked="keyword",x(He,S(";"))):"default"==t?(b.marked="keyword",x(C,S(";"))):"{"==e?x(te(Be,"}"),He,S(";")):h(N)}function Be(e,t){return"as"==t?(b.marked="keyword",x(S("variable"))):"variable"==e?h(W,Be):void 0}function De(e){return"string"==e?x():"("==e?h(C):"."==e?h(U):h(Fe,Ue,He)}function Fe(e,t){return"{"==e?re(Fe,"}"):("variable"==e&&V(t),"*"==t&&(b.marked="keyword"),x(Ge))}function Ue(e){if(","==e)return x(Fe,Ue)}function Ge(e,t){if("as"==t)return b.marked="keyword",x(Fe)}function He(e,t){if("from"==t)return b.marked="keyword",x(C)}function Je(e){return"]"==e?x():h(te(W,"]"))}function Ke(){return h(E("form"),he,S("{"),E("}"),te(Le,"}"),I,I)}function Le(){return h(he,Ve)}return O.lex=_.lex=!0,q.lex=!0,I.lex=!0,{name:e.name,startState:function(t){var r={tokenize:d,lastType:"sof",cc:[],lexical:new y(-t,0,"block",!1),localVars:e.localVars,context:e.localVars&&new T(null,null,!1),indented:0};return e.globalVars&&"object"==typeof e.globalVars&&(r.globalVars=e.globalVars),r},token:function(e,n){if(e.sol()&&(n.lexical.hasOwnProperty("align")||(n.lexical.align=!1),n.indented=e.indentation(),k(e,n)),n.tokenize!=m&&e.eatSpace())return null;var a=n.tokenize(e,n);return"comment"==t?a:(n.lastType="operator"!=t||"++"!=r&&"--"!=r?t:"incdec",function(e,t,r,n,a){var o=e.cc;for(b.state=e,b.stream=a,b.marked=null,b.cc=o,b.style=t,e.lexical.hasOwnProperty("align")||(e.lexical.align=!0);;)if((o.length?o.pop():i?C:N)(r,n)){for(;o.length&&o[o.length-1].lex;)o.pop()();return b.marked?b.marked:"variable"==r&&w(e,n)?"variableName.local":t}}(n,a,t,r,e))},indent:function(t,r,a){if(t.tokenize==m||t.tokenize==p)return null;if(t.tokenize!=d)return 0;var i,o=r&&r.charAt(0),u=t.lexical;if(!/^\s*else\b/.test(r))for(var c=t.cc.length-1;c>=0;--c){var l=t.cc[c];if(l==I)u=u.prev;else if(l!=ze&&l!=q)break}for(;("stat"==u.type||"form"==u.type)&&("}"==o||(i=t.cc[t.cc.length-1])&&(i==U||i==G)&&!/^[,\.=+\-*:?[\(]/.test(r));)u=u.prev;n&&")"==u.type&&"stat"==u.prev.type&&(u=u.prev);var f=u.type,k=o==f;return"vardef"==f?u.indented+("operator"==t.lastType||","==t.lastType?u.info.length+1:0):"form"==f&&"{"==o?u.indented:"form"==f?u.indented+a.unit:"stat"==f?u.indented+(function(e,t){return"operator"==e.lastType||","==e.lastType||s.test(t.charAt(0))||/[,.]/.test(t.charAt(0))}(t,r)?n||a.unit:0):"switch"!=u.info||k||0==e.doubleIndentSwitch?u.align?u.column+(k?0:1):u.indented+(k?0:a.unit):u.indented+(/^(?:case|default)\b/.test(r)?a.unit:2*a.unit)},languageData:{indentOnInput:/^\s*(?:case .*?:|default:|\{|\})$/,commentTokens:i?void 0:{line:"//",block:{open:"/*",close:"*/"}},closeBrackets:{brackets:["(","[","{","'",'"',"`"]},wordChars:"$"}}}const t=e({name:"javascript"}),r=e({name:"json",json:!0}),n=e({name:"json",jsonld:!0}),a=e({name:"typescript",typescript:!0});export{t as javascript,r as json,n as jsonld,a as typescript};
