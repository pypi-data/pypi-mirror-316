"use strict";(self.webpackChunk_N_E=self.webpackChunk_N_E||[]).push([[3528],{43124:function(e,t,n){n.d(t,{Z:function(){return f}});var r=n(24246),i=n(16282),o=n(88038),l=n.n(o),s=n(86677);n(27378);var a=n(11596),u=n(72247),c=n(11032),d=()=>{let e=(0,s.useRouter)();return(0,r.jsx)(i.xuv,{bg:"gray.50",border:"1px solid",borderColor:"blue.400",borderRadius:"md",justifyContent:"space-between",p:5,mb:5,mt:5,children:(0,r.jsxs)(i.xuv,{children:[(0,r.jsxs)(i.Kqy,{direction:{base:"column",sm:"row"},justifyContent:"space-between",children:[(0,r.jsx)(i.xvT,{fontWeight:"semibold",children:"Configure your storage and messaging provider"}),(0,r.jsx)(i.wpx,{onClick:()=>{e.push(c.fz)},children:"Configure"})]}),(0,r.jsxs)(i.xvT,{children:["Before Fides can process your privacy requests we need two simple steps to configure your storage and email client."," "]})]})})},f=e=>{let{children:t,title:n,padded:o=!0,mainProps:c}=e,f=(0,a.hz)(),g=(0,s.useRouter)(),p="/privacy-requests"===g.pathname||"/datastore-connection"===g.pathname,x=!(f.flags.privacyRequestsConfiguration&&p),{data:v}=(0,u.JE)(void 0,{skip:x}),{data:m}=(0,u.PW)(void 0,{skip:x}),b=f.flags.privacyRequestsConfiguration&&(!v||!m)&&p;return(0,r.jsxs)(i.kCb,{"data-testid":n,direction:"column",h:"100vh",children:[(0,r.jsxs)(l(),{children:[(0,r.jsxs)("title",{children:["Fides Admin UI - ",n]}),(0,r.jsx)("meta",{name:"description",content:"Privacy Engineering Platform"}),(0,r.jsx)("link",{rel:"icon",href:"/favicon.ico"})]}),(0,r.jsxs)(i.kCb,{as:"main",direction:"column",py:o?6:0,px:o?10:0,h:o?"calc(100% - 48px)":"full",flex:1,minWidth:0,overflow:"auto",...c,children:[b?(0,r.jsx)(d,{}):null,t]})]})}},6903:function(e,t,n){var r=n(24246),i=n(16282),o=n(60153),l=n(51959),s=n(38565),a=n(27378),u=n(34803),c=n(39514);let d=e=>{let{item:t,label:n,draggable:s,onDeleteItem:a,onRowClick:u,maxH:c=10,rowTestId:d}=e,f=(0,o.o)();return(0,r.jsx)(l.t.Item,{value:t,dragListener:!1,dragControls:f,children:(0,r.jsxs)(i.kCb,{direction:"row",gap:2,maxH:c,w:"full",px:2,align:"center",role:"group",className:"group",borderY:"1px",my:"-1px",borderColor:"gray.200",_hover:u?{bgColor:"gray.100"}:void 0,bgColor:"white",position:"relative",children:[s&&(0,r.jsx)(i.VVU,{onPointerDown:e=>f.start(e),cursor:"grab"}),(0,r.jsx)(i.kCb,{direction:"row",gap:2,p:2,align:"center",w:"full",cursor:u?"pointer":"auto",onClick:()=>{u&&u(t)},overflow:"clip","data-testid":d,children:(0,r.jsx)(i.xvT,{fontSize:"sm",userSelect:"none",textOverflow:"ellipsis",whiteSpace:"nowrap",overflow:"hidden",children:n})}),a&&(0,r.jsx)(i.wpx,{"aria-label":"Delete",onClick:()=>a(t),icon:(0,r.jsx)(i.pJl,{boxSize:3}),size:"small",className:"invisible absolute right-2 bg-white group-hover:visible"})]})})},f=e=>{let{label:t,options:n,onOptionSelected:o,baseTestId:l}=e,[s,u]=(0,a.useState)(!1),[c,d]=(0,a.useState)(void 0);return s?(0,r.jsx)(i.xuv,{w:"full",children:(0,r.jsx)(i.WPr,{showSearch:!0,labelInValue:!0,placeholder:"Select...",filterOption:(e,t)=>{var n;return(null!==(n=null==t?void 0:t.label)&&void 0!==n?n:"").toLowerCase().includes(e.toLowerCase())},value:c,options:n,onChange:e=>{o(e),u(!1),d(void 0)},className:"w-full","data-testid":"select-".concat(l)})}):(0,r.jsx)(i.wpx,{onClick:()=>u(!0),"data-testid":"add-".concat(l),block:!0,icon:(0,r.jsx)(i.jBn,{boxSize:4}),iconPosition:"end",children:t})};t.Z=e=>{let{label:t,tooltip:n,draggable:o,addButtonLabel:a,allItems:g,idField:p,nameField:x=p,values:v,setValues:m,canDeleteItem:b,onRowClick:h,selectOnAdd:j,getItemLabel:w,createNewValue:y,maxHeight:C=36,baseTestId:k}=e,S=e=>e instanceof Object&&p&&p in e?e[p]:e,L=g.every(e=>"string"==typeof e)?g.filter(e=>v.every(t=>t!==e)):g.filter(e=>v.every(t=>S(t)!==S(e))),R=e=>{m(v.filter(t=>t!==e).slice())},_=null!=w?w:e=>e instanceof Object&&p&&p in e?x&&x in e?e[x]:e[p]:e,A=e=>{let t=e instanceof Object&&p&&p in e?e[p]:e;return{label:_(e),value:t}},D=e=>g.every(e=>"string"==typeof e)?e.value:g.find(t=>t[p]===e.value),O=e=>{let t=y?y(e):D(e);m([t,...v.slice()]),j&&h&&h(t)},I={border:"1px",borderColor:"gray.200",borderRadius:"md",w:"full",maxH:"8.5rem",overflowY:"auto"},z=o?(0,r.jsx)(i.xuv,{as:s.E.div,layoutScroll:!0,...I,children:(0,r.jsx)(l.t.Group,{values:v,onReorder:e=>m(e.slice()),children:v.map(e=>{let t=S(e);return(0,r.jsx)(d,{item:e,label:_(e),onDeleteItem:!b||b&&b(e)?R:void 0,onRowClick:h,draggable:!0,maxH:C,rowTestId:"".concat(k,"-row-").concat(t)},t)})})}):(0,r.jsx)(i.xuv,{...I,children:(0,r.jsx)(i.aVo,{children:v.map(e=>{let t=S(e);return(0,r.jsx)(d,{item:e,label:_(e),onRowClick:h,onDeleteItem:R,maxH:C,rowTestId:"".concat(k,"-row-").concat(t)},t)})})});return v.length?(0,r.jsxs)(i.kCb,{align:"start",direction:"column",w:"full",gap:4,children:[t?(0,r.jsx)(u.__,{htmlFor:"test",fontSize:"xs",my:0,mr:1,children:t}):null,n?(0,r.jsx)(c.Z,{label:n}):null,z,L.length?(0,r.jsx)(f,{label:null!=a?a:"Add new",options:L.map(e=>A(e)),onOptionSelected:O,baseTestId:k}):null]}):(0,r.jsx)(f,{label:null!=a?a:"Add new",options:L.map(e=>A(e)),onOptionSelected:O,baseTestId:k})}},60136:function(e,t,n){n.d(t,{D4:function(){return o.D4},MM:function(){return f},Ot:function(){return u},c6:function(){return i},cj:function(){return p},e$:function(){return s},fn:function(){return a},iC:function(){return g},nU:function(){return d},tB:function(){return c}});var r,i,o=n(41164);let l="An unexpected error occurred. Please try again.",s=function(e){let t=arguments.length>1&&void 0!==arguments[1]?arguments[1]:l;if((0,o.Bw)(e)){if((0,o.hE)(e.data))return e.data.detail;if((0,o.cz)(e.data)){var n;let t=null===(n=e.data.detail)||void 0===n?void 0:n[0];return"".concat(null==t?void 0:t.msg,": ").concat(null==t?void 0:t.loc)}if(409===e.status&&(0,o.Dy)(e.data)||404===e.status&&(0,o.XD)(e.data))return"".concat(e.data.detail.error," (").concat(e.data.detail.fides_key,")")}return t};function a(e){return"object"==typeof e&&null!=e&&"status"in e}function u(e){return"object"==typeof e&&null!=e&&"data"in e&&"string"==typeof e.data.detail}function c(e){return"object"==typeof e&&null!=e&&"data"in e&&Array.isArray(e.data.detail)}let d=function(e){let t=arguments.length>1&&void 0!==arguments[1]?arguments[1]:{status:500,message:l};if((0,o.oK)(e))return{status:e.originalStatus,message:e.data};if((0,o.Bw)(e)){let{status:n}=e;return{status:n,message:s(e,t.message)}}return t},f=e=>Object.entries(e).map(e=>({value:e[1],label:e[1]}));(r=i||(i={})).GVL="gvl",r.AC="gacp",r.COMPASS="compass";let g={gvl:{label:"GVL",fullName:"Global Vendor List"},gacp:{label:"AC",fullName:"Google Additional Consent List"},compass:{label:"",fullName:""}},p=e=>{let t=e.split(".")[0];return"gacp"===t?"gacp":"gvl"===t?"gvl":"compass"}},16781:function(e,t,n){n.d(t,{MA:function(){return s},Vo:function(){return u},t5:function(){return a}});var r=n(24246),i=n(16282);let o=e=>{let{children:t}=e;return(0,r.jsxs)(i.xvT,{"data-testid":"toast-success-msg",children:[(0,r.jsx)("strong",{children:"Success:"})," ",t]})},l=e=>{let{children:t}=e;return(0,r.jsxs)(i.xvT,{"data-testid":"toast-error-msg",children:[(0,r.jsx)("strong",{children:"Error:"})," ",t]})},s={variant:"subtle",position:"top",description:"",duration:5e3,status:"success",isClosable:!0},a=e=>{let t=(0,r.jsx)(o,{children:e});return{...s,description:t}},u=e=>{let t=(0,r.jsx)(l,{children:e});return{...s,description:t,status:"error"}}},41164:function(e,t,n){n.d(t,{Bw:function(){return l},D4:function(){return i},Dy:function(){return a},XD:function(){return u},cz:function(){return c},hE:function(){return s},oK:function(){return o}});var r=n(76649);let i=e=>"error"in e,o=e=>(0,r.Ln)({status:"string"},e)&&"PARSING_ERROR"===e.status,l=e=>(0,r.Ln)({status:"number",data:{}},e),s=e=>(0,r.Ln)({detail:"string"},e),a=e=>(0,r.Ln)({detail:{error:"string",resource_type:"string",fides_key:"string"}},e),u=e=>(0,r.Ln)({detail:{error:"string",resource_type:"string",fides_key:"string"}},e),c=e=>(0,r.Ln)({detail:[{loc:["string","number"],msg:"string",type:"string"}]},e)}}]);