(self.webpackChunk_N_E=self.webpackChunk_N_E||[]).push([[2800],{72011:function(e,t,r){var n;n=function(e){return function(e){var t={};function r(n){if(t[n])return t[n].exports;var a=t[n]={i:n,l:!1,exports:{}};return e[n].call(a.exports,a,a.exports,r),a.l=!0,a.exports}return r.m=e,r.c=t,r.i=function(e){return e},r.d=function(e,t,n){r.o(e,t)||Object.defineProperty(e,t,{configurable:!1,enumerable:!0,get:n})},r.n=function(e){var t=e&&e.__esModule?function(){return e.default}:function(){return e};return r.d(t,"a",t),t},r.o=function(e,t){return Object.prototype.hasOwnProperty.call(e,t)},r.p="",r(r.s=3)}([function(e,t,r){"use strict";var n=r(4),a=r(1),i=r(2),o={addUnnecessaryBendpoints:"de.cau.cs.kieler.klay.layered.unnecessaryBendpoints",alignment:"de.cau.cs.kieler.alignment",aspectRatio:"de.cau.cs.kieler.aspectRatio",borderSpacing:"borderSpacing",compactComponents:"de.cau.cs.kieler.klay.layered.components.compact",compactionStrategy:"de.cau.cs.kieler.klay.layered.nodeplace.compactionStrategy",contentAlignment:"de.cau.cs.kieler.klay.layered.contentAlignment",crossingMinimization:"de.cau.cs.kieler.klay.layered.crossMin",cycleBreaking:"de.cau.cs.kieler.klay.layered.cycleBreaking",debugMode:"de.cau.cs.kieler.debugMode",direction:"de.cau.cs.kieler.direction",edgeLabelSideSelection:"de.cau.cs.kieler.klay.layered.edgeLabelSideSelection",edgeRouting:"de.cau.cs.kieler.edgeRouting",edgeSpacingFactor:"de.cau.cs.kieler.klay.layered.edgeSpacingFactor",feedbackEdges:"de.cau.cs.kieler.klay.layered.feedBackEdges",fixedAlignment:"de.cau.cs.kieler.klay.layered.fixedAlignment",greedySwitchCrossingMinimization:"de.cau.cs.kieler.klay.layered.greedySwitch",hierarchyHandling:"de.cau.cs.kieler.hierarchyHandling",inLayerSpacingFactor:"de.cau.cs.kieler.klay.layered.inLayerSpacingFactor",interactiveReferencePoint:"de.cau.cs.kieler.klay.layered.interactiveReferencePoint",layerConstraint:"de.cau.cs.kieler.klay.layered.layerConstraint",layoutHierarchy:"de.cau.cs.kieler.layoutHierarchy",linearSegmentsDeflectionDampening:"de.cau.cs.kieler.klay.layered.linearSegmentsDeflectionDampening",mergeEdges:"de.cau.cs.kieler.klay.layered.mergeEdges",mergeHierarchyCrossingEdges:"de.cau.cs.kieler.klay.layered.mergeHierarchyEdges",noLayout:"de.cau.cs.kieler.noLayout",nodeLabelPlacement:"de.cau.cs.kieler.nodeLabelPlacement",nodeLayering:"de.cau.cs.kieler.klay.layered.nodeLayering",nodePlacement:"de.cau.cs.kieler.klay.layered.nodePlace",portAlignment:"de.cau.cs.kieler.portAlignment",portAlignmentEastern:"de.cau.cs.kieler.portAlignment.east",portAlignmentNorth:"de.cau.cs.kieler.portAlignment.north",portAlignmentSouth:"de.cau.cs.kieler.portAlignment.south",portAlignmentWest:"de.cau.cs.kieler.portAlignment.west",portConstraints:"de.cau.cs.kieler.portConstraints",portLabelPlacement:"de.cau.cs.kieler.portLabelPlacement",portOffset:"de.cau.cs.kieler.offset",portSide:"de.cau.cs.kieler.portSide",portSpacing:"de.cau.cs.kieler.portSpacing",postCompaction:"de.cau.cs.kieler.klay.layered.postCompaction",priority:"de.cau.cs.kieler.priority",randomizationSeed:"de.cau.cs.kieler.randomSeed",routeSelfLoopInside:"de.cau.cs.kieler.selfLoopInside",separateConnectedComponents:"de.cau.cs.kieler.separateConnComp",sizeConstraint:"de.cau.cs.kieler.sizeConstraint",sizeOptions:"de.cau.cs.kieler.sizeOptions",spacing:"de.cau.cs.kieler.spacing",splineSelfLoopPlacement:"de.cau.cs.kieler.klay.layered.splines.selfLoopPlacement",thoroughness:"de.cau.cs.kieler.klay.layered.thoroughness",wideNodesOnMultipleLayers:"de.cau.cs.kieler.klay.layered.wideNodesOnMultipleLayers"},s=function(e){for(var t=Object.keys(e),r={},n=0;n<t.length;n++){var a=t[n],i=o[a],s=e[a];r[i]=s}return r},c={interactiveReferencePoint:"CENTER"},l=function(e){for(var t=e.parent(),r=e.scratch("klay"),n={x:r.x,y:r.y};t.nonempty();){var a=t.scratch("klay");n.x+=a.x,n.y+=a.y,t=t.parent()}return n},d=function(e,t){var r=e.layoutDimensions(t),n=e.numericStyle("padding"),a={_cyEle:e,id:e.id(),padding:{top:n,left:n,bottom:n,right:n}};return e.isParent()||(a.width=r.w,a.height=r.h),e.scratch("klay",a),a},u=function(e,t){var r={_cyEle:e,id:e.id(),source:e.data("source"),target:e.data("target"),properties:{}},n=t.priority(e);return null!=n&&(r.properties.priority=n),e.scratch("klay",r),r},g=function(e,t,r){for(var n=[],a=[],i={},o={id:"root",children:[],edges:[]},s=0;s<e.length;s++){var c=e[s],l=d(c,r);n.push(l),i[c.id()]=l}for(var g=0;g<t.length;g++){var p=t[g],y=u(p,r);a.push(y),i[p.id()]=y}for(var m=0;m<n.length;m++){var f=n[m],k=f._cyEle;if(k.isChild()){var h=i[k.parent().id()];(h.children=h.children||[]).push(f)}else o.children.push(f)}for(var b=0;b<a.length;b++){var v=a[b],S=v._cyEle;S.source().parent(),S.target().parent(),o.edges.push(v)}return o};function p(e){var t=e.klay;this.options=a({},i,e),this.options.klay=a({},i.klay,t,c)}p.prototype.run=function(){var e=this.options,t=e.eles,r=t.nodes(),a=g(r,t.edges(),e);return n.layout({graph:a,options:s(e.klay),success:function(){},error:function(e){throw e}}),r.filter(function(e){return!e.isParent()}).layoutPositions(this,e,l),this},p.prototype.stop=function(){return this},p.prototype.destroy=function(){return this},e.exports=p},function(e,t,r){"use strict";e.exports=null!=Object.assign?Object.assign.bind(Object):function(e){for(var t=arguments.length,r=Array(t>1?t-1:0),n=1;n<t;n++)r[n-1]=arguments[n];return r.filter(function(e){return null!=e}).forEach(function(t){Object.keys(t).forEach(function(r){return e[r]=t[r]})}),e}},function(e,t,r){"use strict";e.exports={nodeDimensionsIncludeLabels:!1,fit:!0,padding:20,animate:!1,animateFilter:function(e,t){return!0},animationDuration:500,animationEasing:void 0,transform:function(e,t){return t},ready:void 0,stop:void 0,klay:{addUnnecessaryBendpoints:!1,aspectRatio:1.6,borderSpacing:20,compactComponents:!1,crossingMinimization:"LAYER_SWEEP",cycleBreaking:"GREEDY",direction:"UNDEFINED",edgeRouting:"ORTHOGONAL",edgeSpacingFactor:.5,feedbackEdges:!1,fixedAlignment:"NONE",inLayerSpacingFactor:1,layoutHierarchy:!1,linearSegmentsDeflectionDampening:.3,mergeEdges:!1,mergeHierarchyCrossingEdges:!0,nodeLayering:"NETWORK_SIMPLEX",nodePlacement:"BRANDES_KOEPF",randomizationSeed:1,routeSelfLoopInside:!1,separateConnectedComponents:!0,spacing:20,thoroughness:7},priority:function(e){return null}}},function(e,t,r){"use strict";var n=r(0),a=function(e){e&&e("layout","klay",n)};"undefined"!=typeof cytoscape&&a(cytoscape),e.exports=a},function(t,r){t.exports=e}])},e.exports=n(r(73552))},2800:function(e,t,r){"use strict";r.r(t),r.d(t,{default:function(){return k}});var n=r(24246),a=r(16282),i=r(27378),o=r(76573),s=r(72011),c=r.n(s),l=r(65218),d=r.n(l),u=r(78622);let g=d()(()=>r.e(7062).then(r.bind(r,37062)),{loadableGenerated:{webpack:()=>[37062]},ssr:!1});o.Z.use(c()),o.Z.warnings(!1);let p=e=>{let{data:t}=e,r=(0,i.useMemo)(()=>[...t.nodes.map(e=>({data:{label:e.name,...e},grabbable:!1,classes:"center-center multiline-auto outline"})),...t.links.map(e=>({data:{source:e.source,target:e.target}}))],[t.links,t.nodes]),n=(0,i.useMemo)(()=>({name:"klay",nodeDimensionsIncludeLabels:!0,klay:{thoroughness:20,borderSpacing:100,direction:"DOWN",edgeRouting:"SPLINES",edgeSpacingFactor:1.3}}),[]),a="#f7fafc";return{elements:r,layoutConfig:n,styleSheet:(0,i.useMemo)(()=>[{selector:"node[label]",style:{label:"data(label)"}},{selector:"node",style:{shape:"ellipse",width:"45px",height:"45px",backgroundColor:a}},{selector:"edge[label]",style:{label:"data(label)",width:3}},{selector:"edge",style:{"curve-style":"bezier","target-arrow-shape":"triangle","line-color":"#888","target-arrow-color":"#888",opacity:.5}},{selector:"node",style:{"background-image":"/images/DatabaseIcon.svg"}},{selector:"node:selected",style:{"background-image":"/images/SelectedDatabaseIcon.svg"}},{selector:".center-center",style:{"text-valign":"center","text-halign":"right"}},{selector:".multiline-auto",style:{"text-wrap":"wrap","text-max-width":"40"}},{selector:".outline",style:{color:"#8d91b4","text-outline-color":"#fff","text-outline-width":1}}],[]),backgroundColor:a}};var y=i.memo(e=>{let{data:t,setSelectedSystemId:r}=e,{elements:o,layoutConfig:s,styleSheet:c,backgroundColor:l}=p({data:t}),d=(0,i.useContext)(u.Y),[y,m]=(0,i.useState)(!1);return(0,i.useEffect)(()=>{let e=e=>{r(e.target._private.data.id)};return d.current&&(d.current.on("click","node",e),d.current.on("layoutstop",()=>{d.current&&(d.current.maxZoom(2.5),d.current.fit(),d.current.maxZoom(100))})),()=>{d.current&&d.current.off("click","node",e)}},[d.current,r]),(0,i.useEffect)(()=>()=>{d.current=void 0},[d]),(0,i.useEffect)(()=>{if(y){var e,t,r,n;null===(e=d.current)||void 0===e||e.layout(s).stop(),null===(t=d.current)||void 0===t||t.layout(s).removeAllListeners(),null===(r=d.current)||void 0===r||r.layout(s),null===(n=d.current)||void 0===n||n.layout(s).run()}},[y,o,d,s]),(0,n.jsx)(a.xuv,{boxSize:"100%","data-testid":"cytoscape-graph",position:"absolute",children:(0,n.jsx)(a.xuv,{boxSize:"100%",bgColor:"gray.50",children:(0,n.jsx)(g,{cy:e=>{y||(m(!0),d.current=e)},elements:o,style:{height:"100%",width:"100%",backgroundColor:l},stylesheet:c,wheelSensitivity:.085,layout:s})})})}),m=r(28401);let f=e=>{let t=(0,i.useMemo)(()=>new Set(null==e?void 0:e.map(e=>e.original["system.fides_key"])),[e]),r=(0,i.useMemo)(()=>e.reduce((e,t)=>{let r=t.original["system.fides_key"];return e[r]||(e[r]={name:t.original["system.name"],description:t.original["system.description"],ingress:t.original["system.ingress"]?t.original["system.ingress"].split(", "):[],egress:t.original["system.egress"]?t.original["system.egress"].split(", "):[],id:t.original["system.fides_key"]}),e},{}),[e]);return{data:(0,i.useMemo)(()=>{let e=[],t=new Set([]);return r&&(e=Object.values(r)).map(e=>[...e.ingress.filter(e=>r[e]).map(t=>({source:t,target:e.id})),...e.egress.filter(e=>r[e]).map(t=>({source:e.id,target:t}))]).flatMap(e=>e).forEach(e=>t.add(JSON.stringify(e))),{nodes:e,links:Array.from(t).map(e=>JSON.parse(e))}},[r]),highlightedNodes:t}};var k=e=>{let{setSelectedSystemId:t}=e,{tableInstance:r}=(0,i.useContext)(m.Z);if(!r)return null;let{rows:o}=r.getRowModel(),{data:s}=f(o);return(0,n.jsx)(a.xuv,{boxSize:"100%",minHeight:"600px",position:"relative",children:(0,n.jsx)(y,{data:s,setSelectedSystemId:t})})}}}]);