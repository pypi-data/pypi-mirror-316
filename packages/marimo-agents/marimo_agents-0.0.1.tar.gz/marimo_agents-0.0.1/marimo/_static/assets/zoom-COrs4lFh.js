function t(t){return((t=Math.exp(t))+1/t)/2}const r=function r(n,a,e){function u(r,u){var h,o,M=r[0],i=r[1],c=r[2],f=u[0],s=u[1],x=u[2],p=f-M,l=s-i,v=p*p+l*l;if(v<1e-12)o=Math.log(x/c)/n,h=function(t){return[M+t*p,i+t*l,c*Math.exp(n*t*o)]};else{var g=Math.sqrt(v),q=(x*x-c*c+e*v)/(2*c*a*g),Q=(x*x-c*c-e*v)/(2*x*a*g),R=Math.log(Math.sqrt(q*q+1)-q),S=Math.log(Math.sqrt(Q*Q+1)-Q);o=(S-R)/n,h=function(r){var e,u=r*o,h=t(R),f=c/(a*g)*(h*(e=n*u+R,((e=Math.exp(2*e))-1)/(e+1))-function(t){return((t=Math.exp(t))-1/t)/2}(R));return[M+f*p,i+f*l,c*h/t(n*u+R)]}}return h.duration=1e3*o*n/Math.SQRT2,h}return u.rho=function(t){var n=Math.max(.001,+t),a=n*n;return r(n,a,a*a)},u}(Math.SQRT2,2,4);export{r as i};
