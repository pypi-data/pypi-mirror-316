import{_ as e,a5 as n,a6 as t,a7 as r,a8 as i,l as a,d as o,a9 as s,aa as d,ab as c,S as l,ac as g,ad as f,ae as p,af as h,ag as u}from"./mermaid-NU_bVGDZ.js";import{G as w}from"./graph-CTPiiFCX.js";import{l as v}from"./layout--KTX9D-V.js";import{w as m}from"./json-Dl_luV-p.js";import"./index-uoOYH9m9.js";import"./transform-B3MLqdQw.js";import"./timer-CK-RIWfW.js";import"./step-CNn2V7Th.js";import"./_baseUniq-Csd1p6bX.js";import"./_baseEach-Ba09ZWYj.js";import"./min-9PgPNNSr.js";import"./_baseMap-B2-gyjtd.js";import"./sortBy-OK1xijHa.js";import"./clone-CkfR8Tgd.js";var y=new Map,X=new Map,b=new Map,E=e((()=>{X.clear(),b.clear(),y.clear()}),"clear"),N=e(((e,n)=>{const t=X.get(n)||[];return a.trace("In isDescendant",n," ",e," = ",t.includes(e)),t.includes(e)}),"isDescendant"),C=e(((e,n)=>{const t=X.get(n)||[];return a.info("Descendants of ",n," is ",t),a.info("Edge is ",e),e.v!==n&&e.w!==n&&(t?t.includes(e.v)||N(e.v,n)||N(e.w,n)||t.includes(e.w):(a.debug("Tilt, ",n,",not in descendants"),!1))}),"edgeInCluster"),x=e(((e,n,t,r)=>{a.warn("Copying children of ",e,"root",r,"data",n.node(e),r);const i=n.children(e)||[];e!==r&&i.push(e),a.warn("Copying (nodes) clusterId",e,"nodes",i),i.forEach((i=>{if(n.children(i).length>0)x(i,n,t,r);else{const o=n.node(i);a.info("cp ",i," to ",r," with parent ",e),t.setNode(i,o),r!==n.parent(i)&&(a.warn("Setting parent",i,n.parent(i)),t.setParent(i,n.parent(i))),e!==r&&i!==e?(a.debug("Setting parent",i,e),t.setParent(i,e)):(a.info("In copy ",e,"root",r,"data",n.node(e),r),a.debug("Not Setting parent for node=",i,"cluster!==rootId",e!==r,"node!==clusterId",i!==e));const s=n.edges(i);a.debug("Copying Edges",s),s.forEach((i=>{a.info("Edge",i);const o=n.edge(i.v,i.w,i.name);a.info("Edge data",o,r);try{C(i,r)?(a.info("Copying as ",i.v,i.w,o,i.name),t.setEdge(i.v,i.w,o,i.name),a.info("newGraph edges ",t.edges(),t.edge(t.edges()[0]))):a.info("Skipping copy of edge ",i.v,"--\x3e",i.w," rootId: ",r," clusterId:",e)}catch(s){a.error(s)}}))}a.debug("Removing node",i),n.removeNode(i)}))}),"copy"),S=e(((e,n)=>{const t=n.children(e);let r=[...t];for(const i of t)b.set(i,e),r=[...r,...S(i,n)];return r}),"extractDescendants"),I=e(((e,n,t)=>{const r=e.edges().filter((e=>e.v===n||e.w===n)),i=e.edges().filter((e=>e.v===t||e.w===t)),a=r.map((e=>({v:e.v===n?t:e.v,w:e.w===n?n:e.w}))),o=i.map((e=>({v:e.v,w:e.w})));return a.filter((e=>o.some((n=>e.v===n.v&&e.w===n.w))))}),"findCommonEdges"),D=e(((e,n,t)=>{const r=n.children(e);if(a.trace("Searching children of id ",e,r),r.length<1)return e;let i;for(const a of r){const e=D(a,n,t),r=I(n,t,e);if(e){if(!(r.length>0))return e;i=e}}return i}),"findNonClusterChild"),j=e((e=>y.has(e)&&y.get(e).externalConnections&&y.has(e)?y.get(e).id:e),"getAnchorId"),O=e(((e,n)=>{if(!e||n>10)a.debug("Opting out, no graph ");else{a.debug("Opting in, graph "),e.nodes().forEach((function(n){e.children(n).length>0&&(a.warn("Cluster identified",n," Replacement id in edges: ",D(n,e,n)),X.set(n,S(n,e)),y.set(n,{id:D(n,e,n),clusterData:e.node(n)}))})),e.nodes().forEach((function(n){const t=e.children(n),r=e.edges();t.length>0?(a.debug("Cluster identified",n,X),r.forEach((e=>{N(e.v,n)^N(e.w,n)&&(a.warn("Edge: ",e," leaves cluster ",n),a.warn("Descendants of XXX ",n,": ",X.get(n)),y.get(n).externalConnections=!0)}))):a.debug("Not a cluster ",n,X)}));for(let n of y.keys()){const t=y.get(n).id,r=e.parent(t);r!==n&&y.has(r)&&!y.get(r).externalConnections&&(y.get(n).id=r)}e.edges().forEach((function(n){const t=e.edge(n);a.warn("Edge "+n.v+" -> "+n.w+": "+JSON.stringify(n)),a.warn("Edge "+n.v+" -> "+n.w+": "+JSON.stringify(e.edge(n)));let r=n.v,i=n.w;if(a.warn("Fix XXX",y,"ids:",n.v,n.w,"Translating: ",y.get(n.v)," --- ",y.get(n.w)),y.get(n.v)||y.get(n.w)){if(a.warn("Fixing and trying - removing XXX",n.v,n.w,n.name),r=j(n.v),i=j(n.w),e.removeEdge(n.v,n.w,n.name),r!==n.v){const i=e.parent(r);y.get(i).externalConnections=!0,t.fromCluster=n.v}if(i!==n.w){const r=e.parent(i);y.get(r).externalConnections=!0,t.toCluster=n.w}a.warn("Fix Replacing with XXX",r,i,n.name),e.setEdge(r,i,t,n.name)}})),a.warn("Adjusted Graph",m(e)),G(e,0),a.trace(y)}}),"adjustClustersAndEdges"),G=e(((e,n)=>{var t,r;if(a.warn("extractor - ",n,m(e),e.children("D")),n>10)return void a.error("Bailing out");let i=e.nodes(),o=!1;for(const a of i){const n=e.children(a);o=o||n.length>0}if(o){a.debug("Nodes = ",i,n);for(const o of i)if(a.debug("Extracting node",o,y,y.has(o)&&!y.get(o).externalConnections,!e.parent(o),e.node(o),e.children("D")," Depth ",n),y.has(o))if(!y.get(o).externalConnections&&e.children(o)&&e.children(o).length>0){a.warn("Cluster without external connections, without a parent and with children",o,n);let i="TB"===e.graph().rankdir?"LR":"TB";(null==(r=null==(t=y.get(o))?void 0:t.clusterData)?void 0:r.dir)&&(i=y.get(o).clusterData.dir,a.warn("Fixing dir",y.get(o).clusterData.dir,i));const s=new w({multigraph:!0,compound:!0}).setGraph({rankdir:i,nodesep:50,ranksep:50,marginx:8,marginy:8}).setDefaultEdgeLabel((function(){return{}}));a.warn("Old graph before copy",m(e)),x(o,e,s,o),e.setNode(o,{clusterNode:!0,id:o,clusterData:y.get(o).clusterData,label:y.get(o).label,graph:s}),a.warn("New graph after copy node: (",o,")",m(s)),a.debug("Old graph after copy",m(e))}else a.warn("Cluster ** ",o," **not meeting the criteria !externalConnections:",!y.get(o).externalConnections," no parent: ",!e.parent(o)," children ",e.children(o)&&e.children(o).length>0,e.children("D"),n),a.debug(y);else a.debug("Not a cluster",o,n);i=e.nodes(),a.warn("New list of nodes",i);for(const t of i){const r=e.node(t);a.warn(" Now next level",t,r),(null==r?void 0:r.clusterNode)&&G(r.graph,n+1)}}else a.debug("Done, no node has children",e.nodes())}),"extractor"),k=e(((e,n)=>{if(0===n.length)return[];let t=Object.assign([],n);return n.forEach((n=>{const r=e.children(n),i=k(e,r);t=[...t,...i]})),t}),"sorter"),B=e((e=>k(e,e.children())),"sortNodesByHierarchy"),P=e((async(n,t,r,i,o,w)=>{a.warn("Graph in recursive render:XAX",m(t),o);const X=t.graph().rankdir;a.trace("Dir in recursive render - dir:",X);const b=n.insert("g").attr("class","root");t.nodes()?a.info("Recursive render XXX",t.nodes()):a.info("No nodes found for",t),t.edges().length>0&&a.info("Recursive edges",t.edge(t.edges()[0]));const E=b.insert("g").attr("class","clusters"),N=b.insert("g").attr("class","edgePaths"),C=b.insert("g").attr("class","edgeLabels"),x=b.insert("g").attr("class","nodes");await Promise.all(t.nodes().map((async function(e){const n=t.node(e);if(void 0!==o){const n=JSON.parse(JSON.stringify(o.clusterData));a.trace("Setting data for parent cluster XXX\n Node.id = ",e,"\n data=",n.height,"\nParent cluster",o.height),t.setNode(o.id,n),t.parent(e)||(a.trace("Setting parent",e,o.id),t.setParent(e,o.id,n))}if(a.info("(Insert) Node XXX"+e+": "+JSON.stringify(t.node(e))),null==n?void 0:n.clusterNode){a.info("Cluster identified XBX",e,n.width,t.node(e));const{ranksep:o,nodesep:c}=t.graph();n.graph.setGraph({...n.graph.graph(),ranksep:o+25,nodesep:c});const l=await P(x,n.graph,r,i,t.node(e),w),g=l.elem;s(n,g),n.diff=l.diff||0,a.info("New compound node after recursive render XAX",e,"width",n.width,"height",n.height),d(g,n)}else t.children(e).length>0?(a.trace("Cluster - the non recursive path XBX",e,n.id,n,n.width,"Graph:",t),a.trace(D(n.id,t)),y.set(n.id,{id:D(n.id,t),node:n})):(a.trace("Node - the non recursive path XAX",e,x,t.node(e),X),await c(x,t.node(e),{config:w,dir:X}))})));const S=e((async()=>{const e=t.edges().map((async function(e){const n=t.edge(e.v,e.w,e.name);a.info("Edge "+e.v+" -> "+e.w+": "+JSON.stringify(e)),a.info("Edge "+e.v+" -> "+e.w+": ",e," ",JSON.stringify(t.edge(e))),a.info("Fix",y,"ids:",e.v,e.w,"Translating: ",y.get(e.v),y.get(e.w)),await u(C,n)}));await Promise.all(e)}),"processEdges");await S(),a.info("Graph before layout:",JSON.stringify(m(t))),a.info("############################################# XXX"),a.info("###                Layout                 ### XXX"),a.info("############################################# XXX"),v(t),a.info("Graph after layout:",JSON.stringify(m(t)));let I=0,{subGraphTitleTotalMargin:j}=l(w);return await Promise.all(B(t).map((async function(e){var n;const r=t.node(e);if(a.info("Position XBX => "+e+": ("+r.x,","+r.y,") width: ",r.width," height: ",r.height),null==r?void 0:r.clusterNode)r.y+=j,a.info("A tainted cluster node XBX1",e,r.id,r.width,r.height,r.x,r.y,t.parent(e)),y.get(r.id).node=r,g(r);else if(t.children(e).length>0){a.info("A pure cluster node XBX1",e,r.id,r.x,r.y,r.width,r.height,t.parent(e)),r.height+=j,t.node(r.parentId);const i=(null==r?void 0:r.padding)/2||0,o=(null==(n=null==r?void 0:r.labelBBox)?void 0:n.height)||0,s=o-i||0;a.debug("OffsetY",s,"labelHeight",o,"halfPadding",i),await f(E,r),y.get(r.id).node=r}else{const e=t.node(r.parentId);r.y+=j/2,a.info("A regular node XBX1 - using the padding",r.id,"parent",r.parentId,r.width,r.height,r.x,r.y,"offsetY",r.offsetY,"parent",e,null==e?void 0:e.offsetY,r),g(r)}}))),t.edges().forEach((function(e){const n=t.edge(e);a.info("Edge "+e.v+" -> "+e.w+": "+JSON.stringify(n),n),n.points.forEach((e=>e.y+=j/2));const o=t.node(e.v);var s=t.node(e.w);const d=p(N,n,y,r,o,s,i);h(n,d)})),t.nodes().forEach((function(e){const n=t.node(e);a.info(e,n.type,n.diff),n.isGroup&&(I=n.diff)})),a.warn("Returning from recursive render XAX",b,I),{elem:b,diff:I}}),"recursiveRender"),J=e((async(e,s)=>{var d,c,l,g,f,p;const h=new w({multigraph:!0,compound:!0}).setGraph({rankdir:e.direction,nodesep:(null==(d=e.config)?void 0:d.nodeSpacing)||(null==(l=null==(c=e.config)?void 0:c.flowchart)?void 0:l.nodeSpacing)||e.nodeSpacing,ranksep:(null==(g=e.config)?void 0:g.rankSpacing)||(null==(p=null==(f=e.config)?void 0:f.flowchart)?void 0:p.rankSpacing)||e.rankSpacing,marginx:8,marginy:8}).setDefaultEdgeLabel((function(){return{}})),u=s.select("g");n(u,e.markers,e.type,e.diagramId),t(),r(),i(),E(),e.nodes.forEach((e=>{h.setNode(e.id,{...e}),e.parentId&&h.setParent(e.id,e.parentId)})),a.debug("Edges:",e.edges),e.edges.forEach((e=>{if(e.start===e.end){const n=e.start,t=n+"---"+n+"---1",r=n+"---"+n+"---2",i=h.node(n);h.setNode(t,{domId:t,id:t,parentId:i.parentId,labelStyle:"",label:"",padding:0,shape:"labelRect",style:"",width:10,height:10}),h.setParent(t,i.parentId),h.setNode(r,{domId:r,id:r,parentId:i.parentId,labelStyle:"",padding:0,shape:"labelRect",label:"",style:"",width:10,height:10}),h.setParent(r,i.parentId);const a=structuredClone(e),o=structuredClone(e),s=structuredClone(e);a.label="",a.arrowTypeEnd="none",a.id=n+"-cyclic-special-1",o.arrowTypeEnd="none",o.id=n+"-cyclic-special-mid",s.label="",i.isGroup&&(a.fromCluster=n,s.toCluster=n),s.id=n+"-cyclic-special-2",h.setEdge(n,t,a,n+"-cyclic-special-0"),h.setEdge(t,r,o,n+"-cyclic-special-1"),h.setEdge(r,n,s,n+"-cyc<lic-special-2")}else h.setEdge(e.start,e.end,{...e},e.id)})),a.warn("Graph at first:",JSON.stringify(m(h))),O(h),a.warn("Graph after XAX:",JSON.stringify(m(h)));const v=o();await P(u,h,e.type,e.diagramId,void 0,v)}),"render");export{J as render};
