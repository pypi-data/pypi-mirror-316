function e(e){for(var t={},n=e.split(" "),r=0;r<n.length;++r)t[n[r]]=!0;return t}var t,n=e("abs acos allnodes ascii asin asstring atan atan2 ave case choose choosen choosesets clustersize combine correlation cos cosh count covariance cron dataset dedup define denormalize distribute distributed distribution ebcdic enth error evaluate event eventextra eventname exists exp failcode failmessage fetch fromunicode getisvalid global graph group hash hash32 hash64 hashcrc hashmd5 having if index intformat isvalid iterate join keyunicode length library limit ln local log loop map matched matchlength matchposition matchtext matchunicode max merge mergejoin min nolocal nonempty normalize parse pipe power preload process project pull random range rank ranked realformat recordof regexfind regexreplace regroup rejected rollup round roundup row rowdiff sample set sin sinh sizeof soapcall sort sorted sqrt stepped stored sum table tan tanh thisnode topn tounicode transfer trim truncate typeof ungroup unicodeorder variance which workunit xmldecode xmlencode xmltext xmlunicode"),r=e("apply assert build buildindex evaluate fail keydiff keypatch loadxml nothor notify output parallel sequential soapcall wait"),a=e("__compressed__ all and any as atmost before beginc++ best between case const counter csv descend encrypt end endc++ endmacro except exclusive expire export extend false few first flat from full function group header heading hole ifblock import in interface joined keep keyed last left limit load local locale lookup macro many maxcount maxlength min skew module named nocase noroot noscan nosort not of only opt or outer overwrite packed partition penalty physicallength pipe quote record relationship repeat return right scan self separator service shared skew skip sql store terminator thor threshold token transform trim true type unicodeorder unsorted validate virtual whole wild within xml xpath"),o=e("ascii big_endian boolean data decimal ebcdic integer pattern qstring real record rule set of string token udecimal unicode unsigned varstring varunicode"),i=e("checkpoint deprecated failcode failmessage failure global independent onwarning persist priority recovery stored success wait when"),l=e("catch class do else finally for if switch try while"),s=e("true false null"),u={"#":function(e,t){return!!t.startOfLine&&(e.skipToEnd(),"meta")}},c=/[+\-*&%=<>!?|\/]/;function p(e,m){var f,h=e.next();if(u[h]){var y=u[h](e,m);if(!1!==y)return y}if('"'==h||"'"==h)return m.tokenize=(f=h,function(e,t){for(var n,r=!1,a=!1;null!=(n=e.next());){if(n==f&&!r){a=!0;break}r=!r&&"\\"==n}return!a&&r||(t.tokenize=p),"string"}),m.tokenize(e,m);if(/[\[\]{}\(\),;\:\.]/.test(h))return t=h,null;if(/\d/.test(h))return e.eatWhile(/[\w\.]/),"number";if("/"==h){if(e.eat("*"))return m.tokenize=d,d(e,m);if(e.eat("/"))return e.skipToEnd(),"comment"}if(c.test(h))return e.eatWhile(c),"operator";e.eatWhile(/[\w\$_]/);var g=e.current().toLowerCase();if(n.propertyIsEnumerable(g))return l.propertyIsEnumerable(g)&&(t="newstatement"),"keyword";if(r.propertyIsEnumerable(g))return l.propertyIsEnumerable(g)&&(t="newstatement"),"variable";if(a.propertyIsEnumerable(g))return l.propertyIsEnumerable(g)&&(t="newstatement"),"modifier";if(o.propertyIsEnumerable(g))return l.propertyIsEnumerable(g)&&(t="newstatement"),"type";if(i.propertyIsEnumerable(g))return l.propertyIsEnumerable(g)&&(t="newstatement"),"builtin";for(var b=g.length-1;b>=0&&(!isNaN(g[b])||"_"==g[b]);)--b;if(b>0){var v=g.substr(0,b+1);if(o.propertyIsEnumerable(v))return l.propertyIsEnumerable(v)&&(t="newstatement"),"type"}return s.propertyIsEnumerable(g)?"atom":null}function d(e,t){for(var n,r=!1;n=e.next();){if("/"==n&&r){t.tokenize=p;break}r="*"==n}return"comment"}function m(e,t,n,r,a){this.indented=e,this.column=t,this.type=n,this.align=r,this.prev=a}function f(e,t,n){return e.context=new m(e.indented,t,n,null,e.context)}function h(e){var t=e.context.type;return")"!=t&&"]"!=t&&"}"!=t||(e.indented=e.context.indented),e.context=e.context.prev}const y={name:"ecl",startState:function(e){return{tokenize:null,context:new m(-e,0,"top",!1),indented:0,startOfLine:!0}},token:function(e,n){var r=n.context;if(e.sol()&&(null==r.align&&(r.align=!1),n.indented=e.indentation(),n.startOfLine=!0),e.eatSpace())return null;t=null;var a=(n.tokenize||p)(e,n);if("comment"==a||"meta"==a)return a;if(null==r.align&&(r.align=!0),";"!=t&&":"!=t||"statement"!=r.type)if("{"==t)f(n,e.column(),"}");else if("["==t)f(n,e.column(),"]");else if("("==t)f(n,e.column(),")");else if("}"==t){for(;"statement"==r.type;)r=h(n);for("}"==r.type&&(r=h(n));"statement"==r.type;)r=h(n)}else t==r.type?h(n):("}"==r.type||"top"==r.type||"statement"==r.type&&"newstatement"==t)&&f(n,e.column(),"statement");else h(n);return n.startOfLine=!1,a},indent:function(e,t,n){if(e.tokenize!=p&&null!=e.tokenize)return 0;var r=e.context,a=t&&t.charAt(0);"statement"==r.type&&"}"==a&&(r=r.prev);var o=a==r.type;return"statement"==r.type?r.indented+("{"==a?0:n.unit):r.align?r.column+(o?0:1):r.indented+(o?0:n.unit)},languageData:{indentOnInput:/^\s*[{}]$/}};export{y as ecl};
