"use strict";(self.webpackChunk_N_E=self.webpackChunk_N_E||[]).push([[8540],{33312:function(e,t,n){var l=n(24246),o=n(16282);t.Z=e=>{let{search:t,onChange:n,withIcon:i,onClear:r,placeholder:s,...a}=e;return(0,l.jsxs)(o.vyj.Compact,{className:"w-96",children:[(0,l.jsx)(o.uFc,{autoComplete:"off",value:t,onChange:e=>n(e.target.value),placeholder:s||"Search...",prefix:i?(0,l.jsx)(o.PTu,{boxSize:4}):void 0,...a}),r?(0,l.jsx)(o.wpx,{onClick:r,children:"Clear"}):null]})}},60136:function(e,t,n){n.d(t,{D4:function(){return i.D4},MM:function(){return g},Ot:function(){return c},c6:function(){return o},cj:function(){return h},e$:function(){return s},fn:function(){return a},iC:function(){return x},nU:function(){return u},tB:function(){return d}});var l,o,i=n(41164);let r="An unexpected error occurred. Please try again.",s=function(e){let t=arguments.length>1&&void 0!==arguments[1]?arguments[1]:r;if((0,i.Bw)(e)){if((0,i.hE)(e.data))return e.data.detail;if((0,i.cz)(e.data)){var n;let t=null===(n=e.data.detail)||void 0===n?void 0:n[0];return"".concat(null==t?void 0:t.msg,": ").concat(null==t?void 0:t.loc)}if(409===e.status&&(0,i.Dy)(e.data)||404===e.status&&(0,i.XD)(e.data))return"".concat(e.data.detail.error," (").concat(e.data.detail.fides_key,")")}return t};function a(e){return"object"==typeof e&&null!=e&&"status"in e}function c(e){return"object"==typeof e&&null!=e&&"data"in e&&"string"==typeof e.data.detail}function d(e){return"object"==typeof e&&null!=e&&"data"in e&&Array.isArray(e.data.detail)}let u=function(e){let t=arguments.length>1&&void 0!==arguments[1]?arguments[1]:{status:500,message:r};if((0,i.oK)(e))return{status:e.originalStatus,message:e.data};if((0,i.Bw)(e)){let{status:n}=e;return{status:n,message:s(e,t.message)}}return t},g=e=>Object.entries(e).map(e=>({value:e[1],label:e[1]}));(l=o||(o={})).GVL="gvl",l.AC="gacp",l.COMPASS="compass";let x={gvl:{label:"GVL",fullName:"Global Vendor List"},gacp:{label:"AC",fullName:"Google Additional Consent List"},compass:{label:"",fullName:""}},h=e=>{let t=e.split(".")[0];return"gacp"===t?"gacp":"gvl"===t?"gvl":"compass"}},56721:function(e,t,n){n.d(t,{_:function(){return o}});var l=n(27378);function o(e,t){let[n,o]=(0,l.useState)(()=>{if(!e)return t;try{let n=window.localStorage.getItem(e);return n?JSON.parse(n):t}catch(e){return console.error(e),t}});return[n,t=>{try{let l=t instanceof Function?t(n):t;o(l),e&&window.localStorage.setItem(e,JSON.stringify(l))}catch(e){console.error(e)}}]}},77650:function(e,t,n){var l=n(24246),o=n(16282);t.Z=e=>{let{isOpen:t,onClose:n,onConfirm:i,onCancel:r,title:s,message:a,cancelButtonText:c,continueButtonText:d,isLoading:u,returnFocusOnClose:g,isCentered:x,testId:h="confirmation-modal",icon:m}=e;return(0,l.jsxs)(o.u_l,{isOpen:t,onClose:n,size:"lg",returnFocusOnClose:null==g||g,isCentered:x,children:[(0,l.jsx)(o.ZAr,{}),(0,l.jsxs)(o.hzk,{textAlign:"center",p:6,"data-testid":h,children:[m?(0,l.jsx)(o.M5Y,{mb:2,children:m}):null,s?(0,l.jsx)(o.xBx,{fontWeight:"medium",pb:0,children:s}):null,a?(0,l.jsx)(o.fef,{children:a}):null,(0,l.jsx)(o.mzw,{children:(0,l.jsxs)(o.MIq,{columns:2,width:"100%",children:[(0,l.jsx)(o.wpx,{onClick:()=>{r&&r(),n()},size:"large",className:"mr-3","data-testid":"cancel-btn",disabled:u,children:c||"Cancel"}),(0,l.jsx)(o.wpx,{type:"primary",size:"large",onClick:i,"data-testid":"continue-btn",loading:u,children:d||"Continue"})]})})]})]})}},54249:function(e,t,n){n.d(t,{W3:function(){return r},bX:function(){return s},oi:function(){return a},s8:function(){return c}});var l=n(24246),o=n(16282),i=n(27378);let r=[25,50,100],s=e=>{let t=e.getFilteredRowModel().rows.length,{pageIndex:n}=e.getState().pagination,{pageSize:l}=e.getState().pagination,o=e.previousPage,i=!e.getCanPreviousPage(),r=e.nextPage,s=!e.getCanNextPage(),{setPageSize:a}=e;return{totalRows:t,onPreviousPageClick:o,isPreviousPageDisabled:i,onNextPageClick:r,isNextPageDisabled:s,setPageSize:a,startRange:n*l==0?1:n*l,endRange:n*l+l}},a=()=>{let[e,t]=(0,i.useState)(r[0]),[n,l]=(0,i.useState)(1),[o,s]=(0,i.useState)(),a=(0,i.useCallback)(()=>{l(e=>e-1)},[l]),c=(0,i.useMemo)(()=>1===n,[n]),d=(0,i.useCallback)(()=>{l(e=>e+1)},[l]),u=(0,i.useMemo)(()=>n===o,[n,o]),g=(n-1)*e==0?1:(n-1)*e,x=(n-1)*e+e,h=(0,i.useCallback)(()=>{l(1)},[]);return{onPreviousPageClick:a,isPreviousPageDisabled:c,onNextPageClick:d,isNextPageDisabled:u,pageSize:e,setPageSize:e=>{t(e),h()},PAGE_SIZES:r,startRange:g,endRange:x,pageIndex:n,resetPageIndexToDefault:h,setTotalPages:s}},c=e=>{let{pageSizes:t,totalRows:n,onPreviousPageClick:i,isPreviousPageDisabled:r,onNextPageClick:s,isNextPageDisabled:a,setPageSize:c,startRange:d,endRange:u}=e;return(0,l.jsxs)(o.Ugi,{ml:1,mt:3,mb:1,children:[(0,l.jsxs)(o.v2r,{children:[(0,l.jsx)(o.j2t,{as:o.wpx,size:"small","data-testid":"pagination-btn",children:(0,l.jsxs)(o.xvT,{fontSize:"xs",lineHeight:4,fontWeight:"semibold",userSelect:"none",style:{fontVariantNumeric:"tabular-nums"},children:[d.toLocaleString("en"),"-",u<=n?u.toLocaleString("en"):n.toLocaleString("en")," ","of ",n.toLocaleString("en")]})}),(0,l.jsx)(o.qyq,{minWidth:"0",children:t.map(e=>(0,l.jsxs)(o.sNh,{onClick:()=>{c(e)},"data-testid":"pageSize-".concat(e),fontSize:"xs",children:[e," per view"]},e))})]}),(0,l.jsx)(o.wpx,{icon:(0,l.jsx)(o.wyc,{}),size:"small","aria-label":"previous page",onClick:i,disabled:r}),(0,l.jsx)(o.wpx,{icon:(0,l.jsx)(o.XCv,{}),size:"small","aria-label":"next page",onClick:s,disabled:a})]})}},98320:function(e,t,n){n.d(t,{A4:function(){return p},CI:function(){return f},Cy:function(){return h},G3:function(){return g},Hm:function(){return w},Rr:function(){return C},S1:function(){return S},WP:function(){return b},k:function(){return j},mb:function(){return v}});var l=n(24246),o=n(8615),i=n(16282),r=n(34090),s=n(27378),a=n(60136),c=n(77650),d=n(16781),u=n(94167);let g=e=>{var t,n;let{value:o,cellProps:r,...s}=e,a=!!(null==r?void 0:null===(t=r.cell.column.columnDef.meta)||void 0===t?void 0:t.showHeaderMenu)&&!!(null==r?void 0:null===(n=r.cellState)||void 0===n?void 0:n.isExpanded);return(0,l.jsx)(i.xvT,{fontSize:"xs",lineHeight:4,py:1.5,fontWeight:"normal",textOverflow:"ellipsis",overflow:a?void 0:"hidden",whiteSpace:a?"normal":void 0,title:a&&o?void 0:null==o?void 0:o.toString(),...s,children:null!=o?o.toString():o})},x=e=>{let{children:t,...n}=e;return(0,l.jsx)(i.Cts,{textTransform:"none",fontWeight:"400",fontSize:"xs",lineHeight:4,color:"gray.600",px:2,py:1,boxShadow:"outline"===n.variant?"inset 0 0 0px 1px var(--chakra-colors-gray-100)":void 0,...n,children:t})},h=e=>{let{time:t}=e;if(!t)return(0,l.jsx)(g,{value:"N/A"});let n=(0,o.Z)(new Date(t),new Date,{addSuffix:!0}),r=(0,u.p6)(new Date(t));return(0,l.jsx)(i.kCb,{alignItems:"center",height:"100%",children:(0,l.jsx)(i.ua7,{label:r,hasArrow:!0,children:(0,l.jsx)(i.xvT,{fontSize:"xs",lineHeight:4,fontWeight:"normal",overflow:"hidden",textOverflow:"ellipsis",children:(0,u.G8)(n)})})})},m=e=>{let{children:t,...n}=e;return(0,l.jsx)(i.kCb,{alignItems:"center",height:"100%",mr:2,...n,children:t})},p=e=>{let{value:t,suffix:n,...o}=e;return(0,l.jsx)(m,{children:(0,l.jsxs)(x,{...o,children:[t,n]})})},f=e=>{let{count:t,singSuffix:n,plSuffix:o,...i}=e,r=null;return r=1===t?(0,l.jsxs)(x,{...i,children:[t,n?" ".concat(n):null]}):(0,l.jsxs)(x,{...i,children:[t,o?" ".concat(o):null]}),(0,l.jsx)(m,{children:r})},v=e=>{let{values:t,cellProps:n,...o}=e,{isExpanded:r,isWrapped:a,version:c}=(null==n?void 0:n.cellState)||{},[d,u]=(0,s.useState)(!r),[g,h]=(0,s.useState)(!!a),[m,p]=(0,s.useState)(r?t:null==t?void 0:t.slice(0,2));return(0,s.useEffect)(()=>{u(!r)},[r,c]),(0,s.useEffect)(()=>{h(!!a)},[a]),(0,s.useEffect)(()=>{(null==t?void 0:t.length)&&p(d?t.slice(0,2):t)},[d,t]),(0,s.useMemo)(()=>(null==m?void 0:m.length)?(0,l.jsxs)(i.kCb,{alignItems:d?"center":"flex-start",flexDirection:d||g?"row":"column",flexWrap:g?"wrap":"nowrap",gap:1.5,pt:2,pb:2,onClick:e=>{d||(e.stopPropagation(),u(!0))},cursor:d?void 0:"pointer",children:[m.map(e=>(0,l.jsx)(x,{"data-testid":e.key,...o,children:e.label},e.key)),d&&t&&t.length>2&&(0,l.jsxs)(i.wpx,{type:"link",size:"small",onClick:()=>u(!1),className:"text-xs font-normal",children:["+",t.length-2," more"]})]}):null,[m,d,g,t,o])},b=e=>{let{value:t,suffix:n,cellState:o,ignoreZero:r,badgeProps:s}=e,a=null;return t?(a=Array.isArray(t)?1===t.length?(0,l.jsx)(x,{...s,children:t}):(null==o?void 0:o.isExpanded)&&t.length>0?t.map((e,t)=>(0,l.jsx)(i.xuv,{mr:2,children:(0,l.jsx)(x,{...s,children:e})},(null==e?void 0:e.toString())||t)):(0,l.jsxs)(x,{...s,children:[t.length,n?" ".concat(n):null]}):(0,l.jsx)(x,{...s,children:t}),(0,l.jsx)(i.kCb,{alignItems:"center",height:"100%",mr:"2",overflowX:"hidden",children:a})):r?null:(0,l.jsxs)(x,{...s,children:["0",n?" ".concat(n):""]})},j=e=>{let{dataTestId:t,...n}=e;return(0,l.jsx)(i.kCb,{alignItems:"center",justifyContent:"center",onClick:e=>e.stopPropagation(),children:(0,l.jsx)(i.XZJ,{"data-testid":t||void 0,...n,colorScheme:"purple"})})},C=e=>{let{value:t,...n}=e;return(0,l.jsx)(i.xvT,{fontSize:"xs",lineHeight:9,fontWeight:"medium",flex:1,...n,children:t})},w=e=>{let{value:t,defaultValue:n,isEditing:o,...s}=e,a=s.column.columnDef.id||"",[c]=(0,r.U$)(a),{submitForm:d}=(0,r.u6)();return o?(0,l.jsx)(i.uFc,{...c,maxLength:80,placeholder:n,"aria-label":"Edit column name",size:"small","data-testid":"column-".concat(a,"-input"),onPressEnter:d}):(0,l.jsx)(C,{value:t,...s})},S=e=>{let{enabled:t,onToggle:n,title:o,message:r,isDisabled:s,...u}=e,g=(0,i.qY0)(),x=(0,i.pmc)(),h=async e=>{let{enable:t}=e,l=await n(t);(0,a.D4)(l)&&x((0,d.Vo)((0,a.e$)(l.error)))},m=async e=>{e?await h({enable:!0}):g.onOpen()};return(0,l.jsxs)(l.Fragment,{children:[(0,l.jsx)(i.rAg,{checked:t,onChange:m,disabled:s,"data-testid":"toggle-switch",...u}),(0,l.jsx)(c.Z,{isOpen:g.isOpen,onClose:g.onClose,onConfirm:()=>{h({enable:!1}),g.onClose()},title:o,message:(0,l.jsx)(i.xvT,{color:"gray.500",children:r}),continueButtonText:"Confirm",isCentered:!0,icon:(0,l.jsx)(i.aNP,{color:"orange.100"})})]})}},8540:function(e,t,n){n.d(t,{A4:function(){return l.A4},CI:function(){return l.CI},F1:function(){return p},G3:function(){return l.G3},Rr:function(){return l.Rr},vr:function(){return W},ZK:function(){return R},HO:function(){return A},WP:function(){return l.WP},k:function(){return l.k},W3:function(){return D.W3},s8:function(){return D.s8},AA:function(){return N},Q$:function(){return O},I4:function(){return _},bX:function(){return D.bX},oi:function(){return D.oi}});var l=n(98320),o=n(24246),i=n(16282),r=n(27378),s=n(71533),a=n(65201),c=n(75383),d=n(52202);let u="DraggableColumnListItem",g=e=>{let{id:t,index:n,moveColumn:l,setColumnVisible:o}=e,i=(0,r.useRef)(null),[{handlerId:s},a]=(0,c.L)({accept:u,collect:e=>({handlerId:e.getHandlerId()}),hover(e,t){var o;if(!i.current)return;let r=e.index;if(r===n)return;let s=null===(o=i.current)||void 0===o?void 0:o.getBoundingClientRect(),a=(s.bottom-s.top)/2,c=t.getClientOffset().y-s.top;r<n&&c<a||r>n&&c>a||(l(r,n),Object.assign(e,{index:n}))}}),[{isDragging:g},x,h]=(0,d.c)({type:u,item:()=>({id:t,index:n}),collect:e=>({isDragging:!!e.isDragging()})});return x(a(i)),{isDragging:g,ref:i,handlerId:s,preview:h,handleColumnVisibleToggle:e=>{o(n,e)}}},x=e=>{let{id:t,index:n,isVisible:l,moveColumn:r,setColumnVisible:s,text:a}=e,{ref:c,isDragging:d,handlerId:u,preview:x,handleColumnVisibleToggle:h}=g({index:n,id:t,moveColumn:r,setColumnVisible:s});return(0,o.jsxs)(i.HCh,{alignItems:"center",display:"flex",minWidth:0,ref:e=>{x(e)},"data-handler-id":u,opacity:d?.2:1,"data-testid":"column-list-item-".concat(t),children:[(0,o.jsx)(i.xuv,{ref:c,cursor:d?"grabbing":"grab","data-testid":"column-dragger-".concat(t),children:(0,o.jsx)(i.DE2,{as:i.zGR,color:"gray.300",flexShrink:0,height:"20px",width:"20px",_hover:{color:"gray.700"}})}),(0,o.jsxs)(i.NIc,{alignItems:"center",display:"flex",minWidth:0,title:a,children:[(0,o.jsx)(i.lXp,{color:"gray.700",fontSize:"normal",fontWeight:400,htmlFor:"".concat(t),mb:"0",minWidth:0,overflow:"hidden",textOverflow:"ellipsis",whiteSpace:"nowrap",flexGrow:1,children:a}),(0,o.jsx)(i.rAg,{id:"".concat(t),checked:l,onChange:h})]})]})},h=e=>{let{columns:t}=e,[n,l]=(0,r.useState)(null!=t?t:[]);return(0,r.useEffect)(()=>{l((null==t?void 0:t.map(e=>({...e})))||[])},[t]),{columns:n,moveColumn:(0,r.useCallback)((e,t)=>{l(n=>(0,a.ZP)(n,n=>{let l=n[e];n.splice(e,1),n.splice(t,0,l)}))},[]),setColumnVisible:(0,r.useCallback)((e,t)=>{l(n=>(0,a.ZP)(n,n=>{n[e]&&(n[e].isVisible=t)}))},[])}},m=e=>{let{columns:t,columnEditor:n}=e;return(0,o.jsx)(i.aVo,{spacing:4,children:t.map((e,t)=>(0,o.jsx)(x,{id:e.id,index:t,isVisible:e.isVisible,moveColumn:n.moveColumn,setColumnVisible:n.setColumnVisible,text:e.displayText},e.id))})},p=e=>{let{isOpen:t,onClose:n,headerText:l,tableInstance:a,columnNameMap:c,prefixColumns:d,savedCustomReportId:u,onColumnOrderChange:g,onColumnVisibilityChange:x}=e,p=h({columns:(0,r.useMemo)(()=>a.getAllColumns().filter(e=>!d.includes(e.id)).map(e=>{var t;return{id:e.id,displayText:(0,s.AH)({columnNameMap:c,columnId:e.id}),isVisible:null!==(t=a.getState().columnVisibility[e.id])&&void 0!==t?t:e.getIsVisible()}}).sort((e,t)=>{let{columnOrder:n}=a.getState(),l=n.indexOf(e.id),o=n.indexOf(t.id);return -1===l&&-1===o?0:-1===l?1:-1===o?-1:l-o}),[u,c])}),f=(0,r.useCallback)(()=>{let e=[...d,...p.columns.map(e=>e.id)],t=p.columns.reduce((e,t)=>(e[t.id]=t.isVisible,e),{});g(e),x(t),n()},[n,d,p.columns,g,x]);return(0,o.jsxs)(i.u_l,{isOpen:t,onClose:n,isCentered:!0,size:"2xl",children:[(0,o.jsx)(i.ZAr,{}),(0,o.jsxs)(i.hzk,{children:[(0,o.jsx)(i.xBx,{pb:0,children:l}),(0,o.jsx)(i.olH,{"data-testid":"column-settings-close-button"}),(0,o.jsxs)(i.fef,{children:[(0,o.jsx)(i.xvT,{fontSize:"sm",color:"gray.500",mb:2,children:"You can toggle columns on and off to hide or show them in the table. Additionally, you can drag columns up or down to change the order"}),(0,o.jsxs)(i.mQc,{colorScheme:"complimentary",children:[(0,o.jsx)(i.tdY,{children:(0,o.jsx)(i.OK9,{color:"complimentary.500",children:"Columns"})}),(0,o.jsx)(i.nPR,{children:(0,o.jsx)(i.x45,{p:0,pt:4,maxHeight:"270px",overflowY:"scroll",children:(0,o.jsx)(m,{columns:p.columns,columnEditor:p})})})]})]}),(0,o.jsx)(i.mzw,{children:(0,o.jsxs)(i.xuv,{display:"flex",justifyContent:"space-between",width:"100%",children:[(0,o.jsx)(i.wpx,{onClick:n,className:"mr-3 grow",children:"Cancel"}),(0,o.jsx)(i.wpx,{onClick:f,type:"primary",className:"grow","data-testid":"save-button",children:"Save"})]})})]})]})};var f=n(59003),v=n(56721),b=n(62528);let j=e=>{var t,n,l,r,a,c;let d,{cell:u,onRowClick:g,cellState:x}=e,h=u.getContext().table.getState().grouping.length>0,m=h?u.getContext().table.getState().grouping[0]:void 0,p=u.column.id===m,v=!1,b=!1,j=!1,C=u.getContext().table.getRowModel().rows.filter(e=>!e.id.includes(":")),w=C[0].id===u.row.id,S=C[C.length-1].id===u.row.id;if(u.getValue()&&p){let e=u.getContext().table.getRow("".concat(u.column.id,":").concat(u.getValue()));j=1===e.subRows.length,v=e.subRows[0].id===u.row.id,b=e.subRows[e.subRows.length-1].id===u.row.id}let y=(!p||v)&&!!(null===(t=u.column.columnDef.meta)||void 0===t?void 0:t.onCellClick);return(null===(n=u.column.columnDef.meta)||void 0===n?void 0:n.disableRowClick)||!g?y&&(d=()=>{var e,t;null===(t=u.column.columnDef.meta)||void 0===t||null===(e=t.onCellClick)||void 0===e||e.call(t,u.row.original)}):d=e=>{g(u.row.original,e)},(0,o.jsx)(i.Td,{width:(null===(l=u.column.columnDef.meta)||void 0===l?void 0:l.width)?u.column.columnDef.meta.width:"unset",overflow:(null===(r=u.column.columnDef.meta)||void 0===r?void 0:r.overflow)?null===(a=u.column.columnDef.meta)||void 0===a?void 0:a.overflow:"auto",borderBottomWidth:S||p?"0px":"1px",borderBottomColor:"gray.200",borderRightWidth:"1px",borderRightColor:"gray.200",sx:{article:{borderTopWidth:"2x",borderTopColor:"red"},...(0,s.J9)(u.column.id),maxWidth:"calc(var(--col-".concat(u.column.id,"-size) * 1px)"),minWidth:"calc(var(--col-".concat(u.column.id,"-size) * 1px)"),"&:hover":{backgroundColor:y?"gray.50":void 0,cursor:y?"pointer":void 0}},_hover:!g||(null===(c=u.column.columnDef.meta)||void 0===c?void 0:c.disableRowClick)?void 0:{cursor:"pointer"},_first:{borderBottomWidth:(h||S)&&(!b||w||S)&&(!v||!j||S)?"0px":"1px"},_last:{borderRightWidth:0},height:"inherit",onClick:d,"data-testid":"row-".concat(u.row.id,"-col-").concat(u.column.id),children:!u.getIsPlaceholder()||v?(0,f.ie)(u.column.columnDef.cell,{...u.getContext(),cellState:x}):null})},C=e=>{let{row:t,renderRowTooltipLabel:n,onRowClick:l,expandedColumns:r,wrappedColumns:a}=e;if(t.getIsGrouped())return null;let c=(0,o.jsx)(i.Tr,{height:"36px",_hover:l?{backgroundColor:"gray.50"}:void 0,"data-testid":"row-".concat(t.id),backgroundColor:t.getCanSelect()?void 0:"gray.50",children:t.getVisibleCells().map(e=>{let t=(0,s.tt)(e.column.id,r),n={isExpanded:!!t&&t>0,isWrapped:!!a.find(t=>t===e.column.id),version:t};return(0,o.jsx)(j,{cell:e,onRowClick:l,cellState:n},e.id)})},t.id);return n?(0,o.jsx)(i.ua7,{label:n?n(t):void 0,hasArrow:!0,placement:"top",children:c}):c},w={asc:{icon:(0,o.jsx)(i.Hf3,{}),title:"Sort ascending"},desc:{icon:(0,o.jsx)(i.veu,{}),title:"Sort descending"}},S={height:i.rSc.space[9],width:"100%",textAlign:"start","&:focus-visible":{backgroundColor:"gray.100"},"&:focus":{outline:"none"}},y=e=>{var t,n,l,r,a,c,d,u;let{header:g,onGroupAll:x,onExpandAll:h,onWrapToggle:m,isExpandAll:p,isWrapped:v,enableSorting:j}=e,{meta:C}=g.column.columnDef;return(null==C?void 0:C.showHeaderMenu)?(0,o.jsxs)(i.v2r,{placement:"bottom-end",closeOnSelect:!C.showHeaderMenuWrapOption,children:[(0,o.jsx)(i.j2t,{as:i.zxk,rightIcon:(0,o.jsxs)(i.Ugi,{children:[null===(t=w[g.column.getIsSorted()])||void 0===t?void 0:t.icon,(0,o.jsx)(i.nXP,{transform:"rotate(90deg)"})]}),title:"Column options",variant:"ghost",size:"sm",sx:{...(0,s.J9)(g.column.id),...S},"data-testid":"".concat(g.id,"-header-menu"),children:(0,f.ie)(g.column.columnDef.header,g.getContext())}),(0,o.jsx)(i.h_i,{children:(0,o.jsxs)(i.qyq,{fontSize:"xs",minW:"0",w:"158px","data-testid":"".concat(g.id,"-header-menu-list"),children:[(0,o.jsxs)(i.sNh,{gap:2,color:p?"complimentary.500":void 0,onClick:()=>h(g.id),children:[(0,o.jsx)(b.oq,{})," Expand all"]}),(0,o.jsxs)(i.sNh,{gap:2,color:p?void 0:"complimentary.500",onClick:()=>x(g.id),children:[(0,o.jsx)(b.Kc,{})," Collapse all"]}),j&&g.column.getCanSort()&&(0,o.jsxs)(i.sNh,{gap:2,onClick:g.column.getToggleSortingHandler(),children:[null!==(d=null===(n=w[g.column.getNextSortingOrder()])||void 0===n?void 0:n.icon)&&void 0!==d?d:(0,o.jsx)(i.Dbz,{}),null!==(u=null===(l=w[g.column.getNextSortingOrder()])||void 0===l?void 0:l.title)&&void 0!==u?u:"Clear sort"]}),C.showHeaderMenuWrapOption&&(0,o.jsxs)(o.Fragment,{children:[(0,o.jsx)(i.RaW,{}),(0,o.jsx)(i.xuv,{px:3,children:(0,o.jsx)(i.XZJ,{size:"sm",isChecked:v,onChange:()=>m(g.id,!v),colorScheme:"complimentary",children:(0,o.jsx)(i.xvT,{fontSize:"xs",children:"Wrap results"})})})]})]})})]}):j&&g.column.getCanSort()?(0,o.jsx)(i.zxk,{"data-testid":"".concat(g.id,"-header-sort"),onClick:g.column.getToggleSortingHandler(),rightIcon:null===(r=w[g.column.getIsSorted()])||void 0===r?void 0:r.icon,title:null!==(c=null===(a=w[g.column.getNextSortingOrder()])||void 0===a?void 0:a.title)&&void 0!==c?c:"Clear sort",variant:"ghost",size:"sm",sx:{...(0,s.J9)(g.column.id),...S},children:(0,f.ie)(g.column.columnDef.header,g.getContext())}):(0,o.jsx)(i.xuv,{"data-testid":"".concat(g.id,"-header"),sx:{...(0,s.J9)(g.column.id)},fontSize:"xs",lineHeight:9,fontWeight:"medium",children:(0,f.ie)(g.column.columnDef.header,g.getContext())})},k=e=>{var t;let{tableInstance:n,rowActionBar:l,onRowClick:r,getRowIsClickable:s,renderRowTooltipLabel:a,expandedColumns:c,wrappedColumns:d,emptyTableNotice:u}=e,g=e=>s?s(e)?r:void 0:r;return(0,o.jsxs)(i.p3B,{"data-testid":"fidesTable-body",children:[l,n.getRowModel().rows.map(e=>(0,o.jsx)(C,{row:e,onRowClick:g(e.original),renderRowTooltipLabel:a,expandedColumns:c,wrappedColumns:d},e.id)),0===n.getRowModel().rows.length&&!(null===(t=n.getState())||void 0===t?void 0:t.globalFilter)&&u&&(0,o.jsx)(i.Tr,{children:(0,o.jsx)(i.Td,{colSpan:100,children:u})})]})},z=r.memo(k,(e,t)=>e.tableInstance.options.data===t.tableInstance.options.data),R=e=>{let{tableInstance:t,rowActionBar:n,footer:l,onRowClick:a,getRowIsClickable:c,renderRowTooltipLabel:d,emptyTableNotice:u,overflow:g="auto",onSort:x,enableSorting:h=!!x,columnExpandStorageKey:m,columnWrapStorageKey:p}=e,[f,b]=(0,r.useState)(1),[j,C]=(0,v._)(m,[]),[w,S]=(0,v._)(p,[]),R=e=>{C([...j.filter(t=>t.split(s.mb)[0]!==e),"".concat(e).concat(s.mb).concat(f)]),b(f+1)},W=e=>{C([...j.filter(t=>t.split(s.mb)[0]!==e),"".concat(e).concat(s.mb).concat(-1*f)]),b(f+1)},I=(e,t)=>{S(t?[...w,e]:w.filter(t=>t!==e))},T=(0,r.useMemo)(()=>{let e=t.getFlatHeaders(),n={};for(let i=0;i<e.length;i+=1){var l,o;let r=e[i],s=!!(null===(l=t.getState().columnSizing)||void 0===l?void 0:l[r.id]),a="auto"===(null===(o=r.column.columnDef.meta)||void 0===o?void 0:o.width);!s&&a?setTimeout(()=>{var e;let l=null===(e=document.getElementById("column-".concat(r.id)))||void 0===e?void 0:e.offsetWidth;l&&(t.setColumnSizing(e=>({...e,[r.id]:l})),n["--header-".concat(r.id,"-size")]=l,n["--col-".concat(r.column.id,"-size")]=l)}):(n["--header-".concat(r.id,"-size")]=r.getSize(),n["--col-".concat(r.column.id,"-size")]=r.column.getSize())}return n},[t.getState().columnSizingInfo]);return(0,r.useEffect)(()=>{x&&x(t.getState().sorting[0])},[t.getState().sorting]),(0,o.jsx)(i.xJi,{"data-testid":"fidesTable",overflowY:g,overflowX:g,borderColor:"gray.200",borderBottomWidth:"1px",borderRightWidth:"1px",borderLeftWidth:"1px",children:(0,o.jsxs)(i.iA_,{variant:"unstyled",style:{borderCollapse:"separate",borderSpacing:0,...T,minWidth:"100%"},children:[(0,o.jsx)(i.hrZ,{position:"sticky",top:"0",height:"36px",zIndex:10,backgroundColor:"gray.50",children:t.getHeaderGroups().map(e=>(0,o.jsx)(i.Tr,{height:"inherit",children:e.headers.map(e=>{let t=(0,s.tt)(e.id,j);return(0,o.jsxs)(i.Th,{borderColor:"gray.200",borderTopWidth:"1px",borderBottomWidth:"1px",borderRightWidth:"1px",_last:{borderRightWidth:0},colSpan:e.colSpan,"data-testid":"column-".concat(e.id),id:"column-".concat(e.id),sx:{padding:0,width:"calc(var(--header-".concat(e.id,"-size) * 1px)"),overflowX:"auto"},textTransform:"unset",position:"relative",_hover:{"& .resizer":{opacity:1}},children:[(0,o.jsx)(y,{header:e,onGroupAll:W,onExpandAll:R,onWrapToggle:I,isExpandAll:!!t&&t>0,isWrapped:!!w.find(t=>e.id===t),enableSorting:h}),e.column.getCanResize()?(0,o.jsx)(i.xuv,{onDoubleClick:()=>e.column.resetSize(),onMouseDown:e.getResizeHandler(),position:"absolute",height:"100%",top:"0",right:"0",width:"5px",cursor:"col-resize",userSelect:"none",className:"resizer",opacity:0,backgroundColor:e.column.getIsResizing()?"complimentary.500":"gray.200"}):null]},e.id)})},e.id))}),t.getState().columnSizingInfo.isResizingColumn?(0,o.jsx)(z,{tableInstance:t,rowActionBar:n,onRowClick:a,getRowIsClickable:c,renderRowTooltipLabel:d,expandedColumns:j,wrappedColumns:w,emptyTableNotice:u}):(0,o.jsx)(k,{tableInstance:t,rowActionBar:n,onRowClick:a,getRowIsClickable:c,renderRowTooltipLabel:d,expandedColumns:j,wrappedColumns:w,emptyTableNotice:u}),l]})})},W=e=>{let{totalColumns:t,children:n}=e;return(0,o.jsx)(i.$RU,{backgroundColor:"gray.50",children:(0,o.jsx)(i.Tr,{children:(0,o.jsx)(i.Td,{colSpan:t,px:4,py:2,borderTop:"1px solid",borderColor:"gray.200",children:n})})})};var I=n(33312),T=n(94167);let A=e=>{let{globalFilter:t,setGlobalFilter:n,placeholder:l,testid:s="global-text-filter"}=e,[a,c]=(0,r.useState)(t),d=(0,r.useMemo)(()=>(0,T.Ds)(n,200),[n]),u=(0,r.useCallback)(()=>{c(void 0),n(void 0)},[c,n]);return(0,r.useEffect)(()=>{a||u()},[a,u]),(0,o.jsx)(i.xuv,{maxWidth:"424px",width:"100%",children:(0,o.jsx)(I.Z,{onChange:e=>{c(e),d(e)},onClear:u,search:a||"",placeholder:l,"data-testid":s})})};var D=n(54249);let N=e=>{let{tableInstance:t,selectedRows:n,isOpen:l}=e;return l?(0,o.jsx)(i.Tr,{position:"sticky",zIndex:"10",top:"36px",backgroundColor:"purple.100",height:"36px",p:0,boxShadow:"0px 4px 6px -1px rgba(0, 0, 0, 0.05)",children:(0,o.jsx)(i.Td,{borderWidth:"1px",borderColor:"gray.200",height:"inherit",pl:4,pr:2,py:0,colSpan:t.getAllColumns().length,children:(0,o.jsxs)(i.Ugi,{children:[(0,o.jsxs)(i.xvT,{"data-testid":"selected-row-count",fontSize:"xs",children:[n.toLocaleString("en")," row(s) selected."]}),t.getIsAllRowsSelected()?null:(0,o.jsxs)(i.wpx,{"data-testid":"select-all-rows-btn",onClick:()=>{t.toggleAllRowsSelected()},type:"link",size:"small",className:"text-xs font-normal text-black underline",children:["Select all ",t.getFilteredRowModel().rows.length," rows."]})]})})}):null},O=e=>{let{children:t,...n}=e;return(0,o.jsx)(i.Ugi,{justifyContent:"space-between",alignItems:"center",p:2,borderWidth:"1px",borderBottomWidth:"0px",borderColor:"gray.200",zIndex:11,...n,children:t})},_=e=>{let{rowHeight:t,numRows:n}=e,l=[];for(let e=0;e<n;e+=1)l.push((0,o.jsx)(i.OdW,{height:"".concat(t,"px")},e));return(0,o.jsx)(i.Kqy,{children:l})}},71533:function(e,t,n){n.d(t,{AH:function(){return c},J9:function(){return s},mb:function(){return r},tt:function(){return a}});var l=n(16282),o=n(98784),i=n.n(o);let r="::",s=e=>"select"===e?{padding:"0px"}:{paddingLeft:l.rSc.space[3],paddingRight:"calc(".concat(l.rSc.space[3]," - 5px)"),paddingTop:"0px",paddingBottom:"0px",borderRadius:"0px"},a=(e,t)=>{let n=t.find(t=>t.startsWith(e));return n?parseInt(n.split(r)[1],10):void 0},c=e=>{let{columnId:t,columnNameMap:n}=e;if(!t)return"";let l=t.replace(/^(system_|privacy_declaration_)/,""),o=i().upperFirst(l.replaceAll("_"," "));return(null==n?void 0:n[t])||o}},16781:function(e,t,n){n.d(t,{MA:function(){return s},Vo:function(){return c},t5:function(){return a}});var l=n(24246),o=n(16282);let i=e=>{let{children:t}=e;return(0,l.jsxs)(o.xvT,{"data-testid":"toast-success-msg",children:[(0,l.jsx)("strong",{children:"Success:"})," ",t]})},r=e=>{let{children:t}=e;return(0,l.jsxs)(o.xvT,{"data-testid":"toast-error-msg",children:[(0,l.jsx)("strong",{children:"Error:"})," ",t]})},s={variant:"subtle",position:"top",description:"",duration:5e3,status:"success",isClosable:!0},a=e=>{let t=(0,l.jsx)(i,{children:e});return{...s,description:t}},c=e=>{let t=(0,l.jsx)(r,{children:e});return{...s,description:t,status:"error"}}},41164:function(e,t,n){n.d(t,{Bw:function(){return r},D4:function(){return o},Dy:function(){return a},XD:function(){return c},cz:function(){return d},hE:function(){return s},oK:function(){return i}});var l=n(76649);let o=e=>"error"in e,i=e=>(0,l.Ln)({status:"string"},e)&&"PARSING_ERROR"===e.status,r=e=>(0,l.Ln)({status:"number",data:{}},e),s=e=>(0,l.Ln)({detail:"string"},e),a=e=>(0,l.Ln)({detail:{error:"string",resource_type:"string",fides_key:"string"}},e),c=e=>(0,l.Ln)({detail:{error:"string",resource_type:"string",fides_key:"string"}},e),d=e=>(0,l.Ln)({detail:[{loc:["string","number"],msg:"string",type:"string"}]},e)}}]);