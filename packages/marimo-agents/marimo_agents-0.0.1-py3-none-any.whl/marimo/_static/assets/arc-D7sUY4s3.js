import{w as n,p as t,c as r,s as c,a as e,h as a,e as u,t as i,b as o,m as y,d as l,f,g as s,i as p,j as x}from"./step-CNn2V7Th.js";function h(n){return n.innerRadius}function g(n){return n.outerRadius}function v(n){return n.startAngle}function d(n){return n.endAngle}function m(n){return n&&n.padAngle}function T(n,t,r,c,e,a,u){var i=n-r,y=t-c,l=(u?a:-a)/o(i*i+y*y),f=l*y,s=-l*i,p=n+f,h=t+s,g=r+f,v=c+s,d=(p+g)/2,m=(h+v)/2,T=g-p,A=v-h,R=T*T+A*A,j=e-a,b=p*v-g*h,w=(A<0?-1:1)*o(x(0,j*j*R-b*b)),P=(b*A-T*w)/R,k=(-b*T-A*w)/R,q=(b*A+T*w)/R,z=(-b*T+A*w)/R,B=P-d,C=k-m,D=q-d,E=z-m;return B*B+C*C>D*D+E*E&&(P=q,k=z),{cx:P,cy:k,x01:-f,y01:-s,x11:P*(e/j-1),y11:k*(e/j-1)}}function A(){var x=h,A=g,R=e(0),j=null,b=v,w=d,P=m,k=null,q=n(z);function z(){var n,e,h=+x.apply(this,arguments),g=+A.apply(this,arguments),v=b.apply(this,arguments)-a,d=w.apply(this,arguments)-a,m=l(d-v),z=d>v;if(k||(k=n=q()),g<h&&(e=g,g=h,h=e),g>u)if(m>i-u)k.moveTo(g*r(v),g*c(v)),k.arc(0,0,g,v,d,!z),h>u&&(k.moveTo(h*r(d),h*c(d)),k.arc(0,0,h,d,v,z));else{var B,C,D=v,E=d,F=v,G=d,H=m,I=m,J=P.apply(this,arguments)/2,K=J>u&&(j?+j.apply(this,arguments):o(h*h+g*g)),L=y(l(g-h)/2,+R.apply(this,arguments)),M=L,N=L;if(K>u){var O=s(K/h*c(J)),Q=s(K/g*c(J));(H-=2*O)>u?(F+=O*=z?1:-1,G-=O):(H=0,F=G=(v+d)/2),(I-=2*Q)>u?(D+=Q*=z?1:-1,E-=Q):(I=0,D=E=(v+d)/2)}var S=g*r(D),U=g*c(D),V=h*r(G),W=h*c(G);if(L>u){var X,Y=g*r(E),Z=g*c(E),$=h*r(F),_=h*c(F);if(m<t)if(X=function(n,t,r,c,e,a,i,o){var y=r-n,l=c-t,f=i-e,s=o-a,p=s*y-f*l;if(!(p*p<u))return[n+(p=(f*(t-a)-s*(n-e))/p)*y,t+p*l]}(S,U,$,_,Y,Z,V,W)){var nn=S-X[0],tn=U-X[1],rn=Y-X[0],cn=Z-X[1],en=1/c(p((nn*rn+tn*cn)/(o(nn*nn+tn*tn)*o(rn*rn+cn*cn)))/2),an=o(X[0]*X[0]+X[1]*X[1]);M=y(L,(h-an)/(en-1)),N=y(L,(g-an)/(en+1))}else M=N=0}I>u?N>u?(B=T($,_,S,U,g,N,z),C=T(Y,Z,V,W,g,N,z),k.moveTo(B.cx+B.x01,B.cy+B.y01),N<L?k.arc(B.cx,B.cy,N,f(B.y01,B.x01),f(C.y01,C.x01),!z):(k.arc(B.cx,B.cy,N,f(B.y01,B.x01),f(B.y11,B.x11),!z),k.arc(0,0,g,f(B.cy+B.y11,B.cx+B.x11),f(C.cy+C.y11,C.cx+C.x11),!z),k.arc(C.cx,C.cy,N,f(C.y11,C.x11),f(C.y01,C.x01),!z))):(k.moveTo(S,U),k.arc(0,0,g,D,E,!z)):k.moveTo(S,U),h>u&&H>u?M>u?(B=T(V,W,Y,Z,h,-M,z),C=T(S,U,$,_,h,-M,z),k.lineTo(B.cx+B.x01,B.cy+B.y01),M<L?k.arc(B.cx,B.cy,M,f(B.y01,B.x01),f(C.y01,C.x01),!z):(k.arc(B.cx,B.cy,M,f(B.y01,B.x01),f(B.y11,B.x11),!z),k.arc(0,0,h,f(B.cy+B.y11,B.cx+B.x11),f(C.cy+C.y11,C.cx+C.x11),z),k.arc(C.cx,C.cy,M,f(C.y11,C.x11),f(C.y01,C.x01),!z))):k.arc(0,0,h,G,F,z):k.lineTo(V,W)}else k.moveTo(0,0);if(k.closePath(),n)return k=null,n+""||null}return z.centroid=function(){var n=(+x.apply(this,arguments)+ +A.apply(this,arguments))/2,e=(+b.apply(this,arguments)+ +w.apply(this,arguments))/2-t/2;return[r(e)*n,c(e)*n]},z.innerRadius=function(n){return arguments.length?(x="function"==typeof n?n:e(+n),z):x},z.outerRadius=function(n){return arguments.length?(A="function"==typeof n?n:e(+n),z):A},z.cornerRadius=function(n){return arguments.length?(R="function"==typeof n?n:e(+n),z):R},z.padRadius=function(n){return arguments.length?(j=null==n?null:"function"==typeof n?n:e(+n),z):j},z.startAngle=function(n){return arguments.length?(b="function"==typeof n?n:e(+n),z):b},z.endAngle=function(n){return arguments.length?(w="function"==typeof n?n:e(+n),z):w},z.padAngle=function(n){return arguments.length?(P="function"==typeof n?n:e(+n),z):P},z.context=function(n){return arguments.length?(k=null==n?null:n,z):k},z}export{A as d};
