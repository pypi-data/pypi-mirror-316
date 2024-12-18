(self.webpackChunk_N_E=self.webpackChunk_N_E||[]).push([[5023],{74245:function(e,t,n){(window.__NEXT_P=window.__NEXT_P||[]).push(["/add-systems",function(){return n(43879)}])},95189:function(e,t,n){"use strict";var s=n(24246),r=n(16282);t.Z=e=>{let{connected:t,...n}=e,i="red.500";return null==t?i="gray.300":t&&(i="green.500"),(0,s.jsx)(r.xuv,{width:"12px",height:"12px",borderRadius:"6px",backgroundColor:i,...n})}},14838:function(e,t,n){"use strict";var s=n(24246),r=n(16282);t.Z=e=>(0,s.jsx)(r.rUS,{isExternal:!0,color:"complimentary.500",...e})},43124:function(e,t,n){"use strict";n.d(t,{Z:function(){return h}});var s=n(24246),r=n(16282),i=n(88038),a=n.n(i),l=n(86677);n(27378);var o=n(11596),c=n(72247),d=n(11032),u=()=>{let e=(0,l.useRouter)();return(0,s.jsx)(r.xuv,{bg:"gray.50",border:"1px solid",borderColor:"blue.400",borderRadius:"md",justifyContent:"space-between",p:5,mb:5,mt:5,children:(0,s.jsxs)(r.xuv,{children:[(0,s.jsxs)(r.Kqy,{direction:{base:"column",sm:"row"},justifyContent:"space-between",children:[(0,s.jsx)(r.xvT,{fontWeight:"semibold",children:"Configure your storage and messaging provider"}),(0,s.jsx)(r.wpx,{onClick:()=>{e.push(d.fz)},children:"Configure"})]}),(0,s.jsxs)(r.xvT,{children:["Before Fides can process your privacy requests we need two simple steps to configure your storage and email client."," "]})]})})},h=e=>{let{children:t,title:n,padded:i=!0,mainProps:d}=e,h=(0,o.hz)(),m=(0,l.useRouter)(),x="/privacy-requests"===m.pathname||"/datastore-connection"===m.pathname,p=!(h.flags.privacyRequestsConfiguration&&x),{data:g}=(0,c.JE)(void 0,{skip:p}),{data:y}=(0,c.PW)(void 0,{skip:p}),j=h.flags.privacyRequestsConfiguration&&(!g||!y)&&x;return(0,s.jsxs)(r.kCb,{"data-testid":n,direction:"column",h:"100vh",children:[(0,s.jsxs)(a(),{children:[(0,s.jsxs)("title",{children:["Fides Admin UI - ",n]}),(0,s.jsx)("meta",{name:"description",content:"Privacy Engineering Platform"}),(0,s.jsx)("link",{rel:"icon",href:"/favicon.ico"})]}),(0,s.jsxs)(r.kCb,{as:"main",direction:"column",py:i?6:0,px:i?10:0,h:i?"calc(100% - 48px)":"full",flex:1,minWidth:0,overflow:"auto",...d,children:[j?(0,s.jsx)(u,{}):null,t]})]})}},78973:function(e,t,n){"use strict";n.d(t,{d:function(){return c}});var s=n(24246),r=n(16282),i=n(34090),a=n(27378),l=n(39514),o=n(34803);let c=e=>{let{name:t,label:n,labelProps:c,tooltip:d,isRequired:u,layout:h="inline",...m}=e,[x,p,{setValue:g}]=(0,i.U$)(t),y=!!(p.touched&&p.error),[j,f]=(0,a.useState)("");x.value||"tags"!==m.mode&&"multiple"!==m.mode||(x.value=[]),"tags"===m.mode&&"string"==typeof x.value&&(x.value=[x.value]);let v="tags"===m.mode?(e,t)=>e?e.value!==j||x.value.includes(j)?m.optionRender?m.optionRender(e,t):e.label:'Create "'.concat(j,'"'):void 0:m.optionRender||void 0,b=e=>{f(e),m.onSearch&&m.onSearch(e)},w=(e,t)=>{g(e),m.onChange&&m.onChange(e,t)};return"inline"===h?(0,s.jsx)(r.NIc,{isInvalid:y,isRequired:u,children:(0,s.jsxs)(r.rjZ,{templateColumns:n?"1fr 3fr":"1fr",children:[n?(0,s.jsx)(o.__,{htmlFor:m.id||t,...c,children:n}):null,(0,s.jsxs)(r.jqI,{align:"center",children:[(0,s.jsxs)(r.jqI,{vertical:!0,flex:1,className:"mr-2",children:[(0,s.jsx)(r.WPr,{...x,id:m.id||t,"data-testid":"controlled-select-".concat(x.name),...m,optionRender:v,onSearch:"tags"===m.mode?b:void 0,onChange:w,value:x.value||void 0}),(0,s.jsx)(o.Bc,{isInvalid:y,message:p.error,fieldName:x.name})]}),d?(0,s.jsx)(l.Z,{label:d}):null]})]})}):(0,s.jsx)(r.NIc,{isInvalid:y,isRequired:u,children:(0,s.jsxs)(r.gCW,{alignItems:"start",children:[(0,s.jsxs)(r.jqI,{align:"center",children:[n?(0,s.jsx)(o.__,{htmlFor:m.id||t,fontSize:"xs",my:0,mr:1,...c,children:n}):null,d?(0,s.jsx)(l.Z,{label:d}):null]}),(0,s.jsx)(r.WPr,{...x,id:m.id||t,"data-testid":"controlled-select-".concat(x.name),...m,optionRender:v,onSearch:"tags"===m.mode?b:void 0,onChange:w,value:x.value||void 0}),(0,s.jsx)(o.Bc,{isInvalid:y,message:p.error,fieldName:x.name})]})})}},60136:function(e,t,n){"use strict";n.d(t,{D4:function(){return i.D4},MM:function(){return h},Ot:function(){return c},c6:function(){return r},cj:function(){return x},e$:function(){return l},fn:function(){return o},iC:function(){return m},nU:function(){return u},tB:function(){return d}});var s,r,i=n(41164);let a="An unexpected error occurred. Please try again.",l=function(e){let t=arguments.length>1&&void 0!==arguments[1]?arguments[1]:a;if((0,i.Bw)(e)){if((0,i.hE)(e.data))return e.data.detail;if((0,i.cz)(e.data)){var n;let t=null===(n=e.data.detail)||void 0===n?void 0:n[0];return"".concat(null==t?void 0:t.msg,": ").concat(null==t?void 0:t.loc)}if(409===e.status&&(0,i.Dy)(e.data)||404===e.status&&(0,i.XD)(e.data))return"".concat(e.data.detail.error," (").concat(e.data.detail.fides_key,")")}return t};function o(e){return"object"==typeof e&&null!=e&&"status"in e}function c(e){return"object"==typeof e&&null!=e&&"data"in e&&"string"==typeof e.data.detail}function d(e){return"object"==typeof e&&null!=e&&"data"in e&&Array.isArray(e.data.detail)}let u=function(e){let t=arguments.length>1&&void 0!==arguments[1]?arguments[1]:{status:500,message:a};if((0,i.oK)(e))return{status:e.originalStatus,message:e.data};if((0,i.Bw)(e)){let{status:n}=e;return{status:n,message:l(e,t.message)}}return t},h=e=>Object.entries(e).map(e=>({value:e[1],label:e[1]}));(s=r||(r={})).GVL="gvl",s.AC="gacp",s.COMPASS="compass";let m={gvl:{label:"GVL",fullName:"Global Vendor List"},gacp:{label:"AC",fullName:"Google Additional Consent List"},compass:{label:"",fullName:""}},x=e=>{let t=e.split(".")[0];return"gacp"===t?"gacp":"gvl"===t?"gvl":"compass"}},53359:function(e,t,n){"use strict";n.d(t,{H:function(){return i},V:function(){return s.V}});var s=n(75139),r=n(60136);let i=()=>{let{errorAlert:e}=(0,s.V)();return{handleError:t=>{let n="An unexpected error occurred. Please try again.";(0,r.Ot)(t)?n=t.data.detail:(0,r.tB)(t)&&(n=t.data.detail[0].msg),e(n)}}}},75139:function(e,t,n){"use strict";n.d(t,{V:function(){return i}});var s=n(24246),r=n(16282);let i=()=>{let e=(0,r.pmc)();return{errorAlert:(t,n,i)=>{let a={...i,position:(null==i?void 0:i.position)||"top",render:e=>{let{onClose:i}=e;return(0,s.jsxs)(r.bZj,{alignItems:"normal",status:"error",children:[(0,s.jsx)(r.zMQ,{}),(0,s.jsxs)(r.xuv,{children:[n&&(0,s.jsx)(r.CdC,{children:n}),(0,s.jsx)(r.XaZ,{children:t})]}),(0,s.jsx)(r.PZ7,{onClick:i,position:"relative",right:0,size:"sm",top:-1})]})}};(null==i?void 0:i.id)&&e.isActive(i.id)?e.update(i.id,a):e(a)},successAlert:(t,n,i)=>{let a={...i,position:(null==i?void 0:i.position)||"top",render:e=>{let{onClose:i}=e;return(0,s.jsxs)(r.bZj,{alignItems:"normal",status:"success",variant:"subtle",children:[(0,s.jsx)(r.zMQ,{}),(0,s.jsxs)(r.xuv,{children:[n&&(0,s.jsx)(r.CdC,{children:n}),(0,s.jsx)(r.XaZ,{children:t})]}),(0,s.jsx)(r.PZ7,{onClick:i,position:"relative",right:0,size:"sm",top:-1})]})}};(null==i?void 0:i.id)&&e.isActive(i.id)?e.update(i.id,a):e(a)}}}},41498:function(e,t,n){"use strict";n.d(t,{V:function(){return i}});var s=n(11596),r=n(11032);let i=()=>({systemOrDatamapRoute:(0,s.hz)().plus?r.oG:r.So})},77650:function(e,t,n){"use strict";var s=n(24246),r=n(16282);t.Z=e=>{let{isOpen:t,onClose:n,onConfirm:i,onCancel:a,title:l,message:o,cancelButtonText:c,continueButtonText:d,isLoading:u,returnFocusOnClose:h,isCentered:m,testId:x="confirmation-modal",icon:p}=e;return(0,s.jsxs)(r.u_l,{isOpen:t,onClose:n,size:"lg",returnFocusOnClose:null==h||h,isCentered:m,children:[(0,s.jsx)(r.ZAr,{}),(0,s.jsxs)(r.hzk,{textAlign:"center",p:6,"data-testid":x,children:[p?(0,s.jsx)(r.M5Y,{mb:2,children:p}):null,l?(0,s.jsx)(r.xBx,{fontWeight:"medium",pb:0,children:l}):null,o?(0,s.jsx)(r.fef,{children:o}):null,(0,s.jsx)(r.mzw,{children:(0,s.jsxs)(r.MIq,{columns:2,width:"100%",children:[(0,s.jsx)(r.wpx,{onClick:()=>{a&&a(),n()},size:"large",className:"mr-3","data-testid":"cancel-btn",disabled:u,children:c||"Cancel"}),(0,s.jsx)(r.wpx,{type:"primary",size:"large",onClick:i,"data-testid":"continue-btn",loading:u,children:d||"Continue"})]})})]})]})}},79541:function(e,t,n){"use strict";var s=n(24246),r=n(16282),i=n(27378);t.Z=e=>{let{handleConfirm:t,isOpen:n,onClose:a,title:l,message:o,confirmButtonText:c="Continue",cancelButtonText:d="Cancel"}=e,u=(0,i.useRef)(null);return(0,s.jsx)(r.aRR,{isOpen:n,leastDestructiveRef:u,onClose:a,children:(0,s.jsx)(r.dhV,{children:(0,s.jsxs)(r._Tf,{alignItems:"center",textAlign:"center",children:[(0,s.jsx)(r.aNP,{marginTop:3}),(0,s.jsx)(r.fYl,{fontSize:"lg",fontWeight:"bold",children:l}),(0,s.jsx)(r.iPF,{pt:0,children:o}),(0,s.jsxs)(r.xoY,{children:[(0,s.jsx)(r.wpx,{ref:u,onClick:a,size:"large",children:d}),(0,s.jsx)(r.wpx,{onClick:()=>t(),type:"primary",size:"large",className:"ml-3","data-testid":"warning-modal-confirm-btn",children:c})]})]})})})}},16781:function(e,t,n){"use strict";n.d(t,{MA:function(){return l},Vo:function(){return c},t5:function(){return o}});var s=n(24246),r=n(16282);let i=e=>{let{children:t}=e;return(0,s.jsxs)(r.xvT,{"data-testid":"toast-success-msg",children:[(0,s.jsx)("strong",{children:"Success:"})," ",t]})},a=e=>{let{children:t}=e;return(0,s.jsxs)(r.xvT,{"data-testid":"toast-error-msg",children:[(0,s.jsx)("strong",{children:"Error:"})," ",t]})},l={variant:"subtle",position:"top",description:"",duration:5e3,status:"success",isClosable:!0},o=e=>{let t=(0,s.jsx)(i,{children:e});return{...l,description:t}},c=e=>{let t=(0,s.jsx)(a,{children:e});return{...l,description:t,status:"error"}}},43879:function(e,t,n){"use strict";n.r(t),n.d(t,{default:function(){return ea}});var s=n(24246),r=n(27378),i=n(44296),a=n(43124),l=n(86564),o=n(16282),c=n(86677),d=n(11596),u=n(62528),h=n(77650);let m=e=>{let{onCancel:t,onConfirm:n,isOpen:r,onClose:i}=e;return(0,s.jsx)(h.Z,{isOpen:r,onClose:i,onCancel:t,isCentered:!0,title:"Upgrade to choose vendors",message:"To choose vendors and have system information auto-populated using Fides Compass, you will need to upgrade Fides. Meanwhile, you can manually add individual systems using the button below.",cancelButtonText:"Add vendors manually",continueButtonText:"Upgrade",onConfirm:n})};var x=n(11032),p=n(10284),g=n(95189),y=n(96878);let j=e=>{let{label:t,description:n,icon:r,onClick:i,...a}=e;return(0,s.jsx)(o.wpx,{type:"text",onClick:i,className:"h-full min-h-[116px] rounded-lg border border-gray-300 p-4",...a,children:(0,s.jsxs)(o.xuv,{as:"span",display:"flex",flexDirection:"column",alignItems:"start",justifyContent:"space-between",height:"100%",width:"100%",whiteSpace:"break-spaces",textAlign:"left",children:[(0,s.jsxs)(o.xuv,{as:"span",display:"flex",alignItems:"center",mb:2,children:[r,(0,s.jsx)(o.xvT,{fontWeight:"semibold",color:"gray.700",as:"span",ml:3,children:t})]}),(0,s.jsx)(o.xvT,{color:"gray.500",as:"span",fontWeight:"medium",children:n})]})})},f=e=>{var t;let{onClick:n}=e,{plus:r,dataFlowScanning:a}=(0,d.hz)(),l=(0,i.C)(y.bw),c=null!==(t=null==l?void 0:l.cluster_health)&&void 0!==t?t:"unknown",h=c===p.wW.HEALTHY;if(!r)return null;let m="";a?h||(m="Your cluster appears not to be healthy. Its status is ".concat(c,".")):m="The data flow scanner is not enabled, please check your configuration.";let x=!a||!h;return(0,s.jsxs)(o.xuv,{position:"relative",children:[(0,s.jsx)(j,{label:"Data flow scan",description:"Automatically discover new systems in your Kubernetes infrastructure",icon:(0,s.jsx)(u.pt,{boxSize:8}),onClick:n,disabled:x,title:x?m:void 0,"data-testid":"data-flow-scan-btn"}),a?(0,s.jsx)(g.Z,{connected:h,title:h?"Cluster is connected and healthy":"Cluster is ".concat(c),position:"absolute",right:-1,top:-1,"data-testid":"cluster-health-indicator"}):null]})};var v=n(58697);let b=e=>{let{children:t}=e;return(0,s.jsx)(o.X6q,{as:"h4",size:"xs",fontWeight:"semibold",color:"gray.600",textTransform:"uppercase",mb:4,children:t})};var w=()=>{let e=(0,i.T)(),t=(0,c.useRouter)(),{isOpen:n,onClose:r,onOpen:a}=(0,o.qY0)(),{dictionaryService:h}=(0,d.hz)();return(0,s.jsxs)(o.Kqy,{spacing:9,"data-testid":"add-systems",children:[(0,s.jsxs)(o.Kqy,{spacing:6,maxWidth:"600px",children:[(0,s.jsx)(o.X6q,{as:"h3",size:"lg",fontWeight:"semibold",children:"Fides helps you map your systems to manage your privacy"}),(0,s.jsx)(o.xvT,{children:"In Fides, systems describe any services that store or process data for your organization, including third-party APIs, web applications, databases, and data warehouses."}),(0,s.jsx)(o.xvT,{children:"Fides can automatically discover new systems in your AWS infrastructure or Okta accounts. For services not covered by the automated scanners or analog processes, you may also manually add new systems to your map."})]}),(0,s.jsx)(m,{isOpen:n,onConfirm:()=>{window.open("https://fid.es/upgrade-compass")},onCancel:()=>{t.push(x.N5)},onClose:r}),(0,s.jsxs)(o.xuv,{"data-testid":"manual-options",children:[(0,s.jsx)(b,{children:"Manually add systems"}),(0,s.jsxs)(o.MIq,{columns:{base:1,md:2,xl:3},spacing:"4",children:[(0,s.jsx)(j,{label:"Add a system",icon:(0,s.jsx)(u.P$,{boxSize:8}),description:"Manually add a system for services not covered by automated scanners",onClick:()=>{e((0,l.CQ)(v.D.MANUAL)),t.push(x.N5)},"data-testid":"manual-btn"}),(0,s.jsx)(j,{label:"Add multiple systems",icon:(0,s.jsx)(u.P$,{boxSize:8}),description:"Choose vendors and automatically populate system details",onClick:()=>{h?(e((0,l.CQ)(v.D.MANUAL)),t.push(x.bJ)):a()},"data-testid":"multiple-btn"})]})]}),(0,s.jsxs)(o.xuv,{"data-testid":"automated-options",children:[(0,s.jsx)(b,{children:"Automated infrastructure scanning"}),(0,s.jsxs)(o.MIq,{columns:{base:1,md:2,xl:3},spacing:"4",children:[(0,s.jsx)(j,{label:"Scan your infrastructure (AWS)",description:"Automatically discover new systems in your AWS infrastructure",icon:(0,s.jsx)(u.bj,{boxSize:8}),onClick:()=>{e((0,l.CQ)(p.GC.AWS)),e((0,l.sz)())},"data-testid":"aws-btn"}),(0,s.jsx)(j,{label:"Scan your Sign On Provider (Okta)",description:"Automatically discover new systems in your Okta infrastructure",icon:(0,s.jsx)(u.tb,{boxSize:8}),onClick:()=>{e((0,l.CQ)(p.GC.OKTA)),e((0,l.sz)())},"data-testid":"okta-btn"}),(0,s.jsx)(f,{onClick:()=>{e((0,l.sz)()),e((0,l.CQ)(v.D.DATA_FLOW))}})]})]})]})},C=n(34090),k=n(59389),S=n(34803),_=n(60136),A=n(53359),T=n(78973),z=n(31332);let q=e=>"system_type"in e,{useGenerateMutation:O}=n(21618).u.injectEndpoints({endpoints:e=>({generate:e.mutation({query:e=>({url:"generate",method:"POST",body:e})})})});var I=n(14838);let D=e=>{let{message:t}=e;return(0,s.jsxs)(s.Fragment,{children:[(0,s.jsx)(o.izJ,{}),(0,s.jsx)(o.W20,{maxH:"50vh",overflow:"auto",children:(0,s.jsx)(o.xvT,{as:"pre","data-testid":"error-log",children:t})}),(0,s.jsx)(o.izJ,{})]})};var W=e=>{let{error:t,scanType:n=""}=e;return(0,s.jsxs)(o.Kqy,{"data-testid":"scanner-error",spacing:"4",children:[(0,s.jsxs)(o.Ugi,{children:[(0,s.jsx)(o.Cts,{color:"white",bg:"red.500",py:"2",children:"Error"}),(0,s.jsx)(o.X6q,{color:"red.500",size:"lg",children:"Failed to Scan"})]}),403===t.status&&n===p.GC.AWS?(0,s.jsxs)(s.Fragment,{children:[(0,s.jsx)(o.xvT,{"data-testid":"permission-msg",children:"Fides was unable to scan AWS. It appears that the credentials were valid to login but they did not have adequate permission to complete the scan."}),(0,s.jsxs)(o.xvT,{children:["To fix this issue, double check that you have granted"," ",(0,s.jsx)(I.Z,{href:z.zu,children:"the required permissions"})," ","to these credentials as part of your IAM policy. If you need more help in configuring IAM policies, you can read about them"," ",(0,s.jsx)(I.Z,{href:"https://docs.aws.amazon.com/IAM/latest/UserGuide/introduction_access-management.html",children:"here"}),"."]})]}):(0,s.jsxs)(s.Fragment,{children:[(0,s.jsx)(o.xvT,{"data-testid":"generic-msg",children:"Fides was unable to scan your infrastructure. Please ensure your credentials are accurate and inspect the error log below for more details."}),(0,s.jsx)(D,{message:t.message}),(0,s.jsxs)(o.xvT,{children:["If this error does not clarify why scanning failed, please"," ",(0,s.jsx)(I.Z,{href:z.we,children:"create a new issue"}),"."]})]})]})},F=n(79541);let R=(0,s.jsxs)(s.Fragment,{children:[(0,s.jsx)(o.xvT,{color:"gray.500",mb:3,children:"Warning, you are about to cancel the scan!"}),(0,s.jsx)(o.xvT,{color:"gray.500",mb:3,children:"If you cancel scanning, the scanner will stop and no systems will be returned."}),(0,s.jsx)(o.xvT,{color:"gray.500",mb:3,children:"Are you sure you want to cancel?"})]});var N=e=>{let{title:t,onClose:n}=e,{isOpen:r,onOpen:i,onClose:a}=(0,o.qY0)();return(0,s.jsxs)(s.Fragment,{children:[(0,s.jsxs)(o.Kqy,{spacing:8,"data-testid":"scanner-loading",children:[(0,s.jsxs)(o.Ugi,{children:[(0,s.jsx)(o.xvT,{alignItems:"center",as:"b",color:"gray.900",display:"flex",fontSize:"xl",children:t}),(0,s.jsx)(o.PZ7,{"data-testid":"close-scan-in-progress",display:"inline-block",onClick:i})]}),(0,s.jsx)(o.Kqy,{alignItems:"center",children:(0,s.jsx)(o.$jN,{thickness:"4px",speed:"0.65s",emptyColor:"gray.200",color:"green.300",size:"xl"})})]}),(0,s.jsx)(F.Z,{isOpen:r,onClose:a,handleConfirm:n,title:"Cancel Scan!",message:R,confirmButtonText:"Yes, Cancel",cancelButtonText:"No, Continue Scanning"})]})};let Z={aws_access_key_id:"",aws_secret_access_key:"",aws_session_token:"",region_name:""},K=k.Ry().shape({aws_access_key_id:k.Z_().required().trim().matches(/^\w+$/,"Cannot contain spaces or special characters").label("Access Key ID"),aws_secret_access_key:k.Z_().required().trim().matches(/^[^\s]+$/,"Cannot contain spaces").label("Secret"),aws_session_token:k.Z_().optional().trim().matches(/^[^\s]+$/,"Cannot contain spaces").label("Session Token (for temporary credentials)"),region_name:k.Z_().required().label("Default Region")});var B=()=>{let e=(0,i.C)(l.De),t=(0,i.T)(),{successAlert:n}=(0,A.V)(),[a,c]=(0,r.useState)(),d=e=>{let s=(null!=e?e:[]).filter(q);t((0,l.un)(s)),t((0,l.sz)()),n("Your scan was successfully completed, with ".concat(s.length," new systems detected!"),"Scan Successfully Completed",{isClosable:!0})},u=e=>{c((0,_.nU)(e,{status:500,message:"Our system encountered a problem while connecting to AWS."}))},h=()=>{t((0,l.sz)(2))},[m,{isLoading:x}]=O(),g=async t=>{c(void 0);let n=await m({organization_key:e,generate:{config:t,target:p.GC.AWS,type:p.j.SYSTEMS}});(0,_.D4)(n)?u(n.error):d(n.data.generate_results)};return(0,s.jsx)(C.J9,{initialValues:Z,validationSchema:K,onSubmit:g,children:e=>{let{isValid:t,isSubmitting:n,dirty:r}=e;return(0,s.jsx)(C.l0,{"data-testid":"authenticate-aws-form",children:(0,s.jsxs)(o.Kqy,{spacing:10,children:[n?(0,s.jsx)(N,{title:"System scanning in progress",onClose:h}):null,a?(0,s.jsx)(W,{error:a,scanType:"aws"}):null,n||a?null:(0,s.jsxs)(s.Fragment,{children:[(0,s.jsx)(o.X6q,{size:"lg",children:"Authenticate AWS Scanner"}),(0,s.jsx)("h2",{children:"To use the scanner to inventory systems in AWS, you must first authenticate to your AWS cloud by providing the following information:"}),(0,s.jsxs)(o.Kqy,{children:[(0,s.jsx)(S.j0,{name:"aws_access_key_id",label:"Access Key ID",tooltip:"The Access Key ID created by the cloud hosting provider.",isRequired:!0}),(0,s.jsx)(S.j0,{type:"password",name:"aws_secret_access_key",label:"Secret",tooltip:"The secret associated with the Access Key ID used for authentication.",isRequired:!0}),(0,s.jsx)(S.j0,{type:"password",name:"aws_session_token",label:"Session Token",tooltip:"The session token when using temporary credentials."}),(0,s.jsx)(T.d,{name:"region_name",label:"AWS Region",tooltip:"The geographic region of the cloud hosting provider you would like to scan.",options:z.xO,isRequired:!0,placeholder:"Select a region"})]})]}),n?null:(0,s.jsxs)(o.Ugi,{children:[(0,s.jsx)(o.wpx,{onClick:h,children:"Cancel"}),(0,s.jsx)(o.wpx,{htmlType:"submit",type:"primary",disabled:!r||!t,loading:x,"data-testid":"submit-btn",children:"Save and continue"})]})]})})}})};let E={orgUrl:"",token:""},U=k.Ry().shape({orgUrl:k.Z_().required().trim().url().label("URL"),token:k.Z_().required().trim().matches(/^[^\s]+$/,"Cannot contain spaces").label("Token")});var M=()=>{let e=(0,i.C)(l.De),t=(0,i.T)(),{successAlert:n}=(0,A.V)(),[a,c]=(0,r.useState)(),d=e=>{let s=(null!=e?e:[]).filter(q);t((0,l.un)(s)),t((0,l.sz)()),n("Your scan was successfully completed, with ".concat(s.length," new systems detected!"),"Scan Successfully Completed",{isClosable:!0})},u=e=>{c((0,_.nU)(e,{status:500,message:"Our system encountered a problem while connecting to Okta."}))},h=()=>{t((0,l.sz)(2))},[m,{isLoading:x}]=O(),g=async t=>{c(void 0);let n=await m({organization_key:e,generate:{config:t,target:p.GC.OKTA,type:p.j.SYSTEMS}});(0,_.D4)(n)?u(n.error):d(n.data.generate_results)};return(0,s.jsx)(C.J9,{initialValues:E,validationSchema:U,onSubmit:g,children:e=>{let{isValid:t,isSubmitting:n,dirty:r}=e;return(0,s.jsx)(C.l0,{"data-testid":"authenticate-okta-form",children:(0,s.jsxs)(o.Kqy,{spacing:10,children:[n?(0,s.jsx)(N,{title:"System scanning in progress",onClose:h}):null,a?(0,s.jsx)(W,{error:a}):null,n||a?null:(0,s.jsxs)(s.Fragment,{children:[(0,s.jsx)(o.X6q,{size:"lg",children:"Authenticate Okta Scanner"}),(0,s.jsx)("h2",{children:"To use the scanner to inventory systems in Okta, you must first authenticate to your Okta account by providing the following information:"}),(0,s.jsxs)(o.Kqy,{children:[(0,s.jsx)(S.j0,{name:"orgUrl",label:"Domain",tooltip:"The URL for your organization's account on Okta"}),(0,s.jsx)(S.j0,{name:"token",label:"Okta token",type:"password",tooltip:"The token generated by Okta for your account."})]})]}),n?null:(0,s.jsxs)(o.Ugi,{children:[(0,s.jsx)(o.wpx,{onClick:h,children:"Cancel"}),(0,s.jsx)(o.wpx,{htmlType:"submit",type:"primary",disabled:!r||!t,loading:x,"data-testid":"submit-btn",children:"Save and continue"})]})]})})}})},P=n(16781),L=n(43073),X=()=>{let e=(0,i.T)(),t=(0,o.pmc)(),[n]=(0,y.J9)(),[a,{data:c}]=(0,y.KW)(),[d,u]=(0,r.useState)(),[h,m]=(0,r.useState)(!1),x=e=>{u((0,_.nU)(e,{status:500,message:"Our system encountered a problem while scanning your infrastructure."}))};(0,r.useEffect)(()=>{(async()=>{let{error:e}=await n();m(!(e&&(0,L.Bw)(e)&&404===e.status));let t=await a({classify:!0});(0,_.D4)(t)&&x(t.error)})()},[a,n]),(0,r.useEffect)(()=>{(async()=>{if(c){let{data:s}=await n(),r=h?(null==s?void 0:s.added_systems)||[]:c.systems;t((0,P.t5)("Your scan was successfully completed, with ".concat(r.length," new systems detected!"))),e((0,l.un)(r)),e((0,l.sz)())}})()},[c,t,e,h,n]);let p=()=>{e((0,l.sz)(2))};return d?(0,s.jsxs)(o.Kqy,{children:[(0,s.jsx)(W,{error:d}),(0,s.jsx)(o.xuv,{children:(0,s.jsx)(o.wpx,{onClick:p,"data-testid":"cancel-btn",children:"Cancel"})})]}):(0,s.jsx)(N,{title:"Infrastructure scanning in progress",onClose:p})},V=()=>{let e=(0,i.C)(l.Ll);return(0,s.jsxs)(o.xuv,{w:"40%",children:[e===p.GC.AWS?(0,s.jsx)(B,{}):null,e===p.GC.OKTA?(0,s.jsx)(M,{}):null,e===v.D.DATA_FLOW?(0,s.jsx)(X,{}):null]})},G=n(36701);let Y=()=>{var e,t;let n=(0,i.T)(),s=e=>{n((0,l.nD)(e)),n((0,l.sz)())},[a]=(0,G.vz)(),[c]=(0,G.$f)(),{data:d,isLoading:u}=(0,G.GQ)(G.Av),[h,m]=(0,r.useState)(!1);(0,r.useEffect)(()=>{!u&&!h&&(null==d?void 0:d.name)&&(null==d?void 0:d.description)&&n((0,l.sz)())},[u,d,n,h]);let x=(0,o.pmc)();return(0,C.TA)({initialValues:{name:null!==(e=null==d?void 0:d.name)&&void 0!==e?e:"",description:null!==(t=null==d?void 0:d.description)&&void 0!==t?t:""},onSubmit:async e=>{var t,n,r;m(!0);let i={name:null!==(t=e.name)&&void 0!==t?t:null==d?void 0:d.name,description:null!==(n=e.description)&&void 0!==n?n:null==d?void 0:d.description,fides_key:null!==(r=null==d?void 0:d.fides_key)&&void 0!==r?r:G.Av,organization_fides_key:G.Av};if(d){let e=await c(i);if((0,_.D4)(e)){x({status:"error",description:(0,_.e$)(e.error)});return}x.closeAll(),s(i)}else{let e=await a(i);if((0,_.D4)(e)){x({status:"error",description:(0,_.e$)(e.error)});return}x.closeAll(),s(i)}},enableReinitialize:!0,validate:e=>{let t={};return e.name||(t.name="Organization name is required"),e.description||(t.description="Organization description is required"),t}})};var $=()=>{let{errors:e,handleBlur:t,handleChange:n,handleSubmit:r,touched:i,values:a,isSubmitting:l}=Y();return(0,s.jsx)(o.m$N.form,{onSubmit:r,w:"40%","data-testid":"organization-info-form",children:(0,s.jsxs)(o.Kqy,{spacing:10,children:[(0,s.jsx)(o.X6q,{as:"h3",size:"lg",children:"Create your Organization"}),(0,s.jsx)("div",{children:"Provide your organization information. This information is used to configure your organization in Fides for data map reporting purposes."}),(0,s.jsx)(o.Kqy,{children:(0,s.jsxs)(o.NIc,{children:[(0,s.jsxs)(o.Kqy,{direction:"row",mb:5,justifyContent:"flex-end",children:[(0,s.jsx)(o.lXp,{w:"100%",children:"Organization name"}),(0,s.jsx)(o.IIB,{type:"text",id:"name",name:"name",focusBorderColor:"gray.700",onChange:n,onBlur:t,value:a.name,isInvalid:i.name&&!!e.name,minW:"65%",w:"65%","data-testid":"input-name"}),(0,s.jsx)(o.ua7,{fontSize:"md",label:"The legal name of your organization",placement:"right",children:(0,s.jsx)(o.UOT,{boxSize:5,color:"gray.400"})})]}),(0,s.jsxs)(o.Kqy,{direction:"row",justifyContent:"flex-end",children:[(0,s.jsx)(o.lXp,{w:"100%",children:"Description"}),(0,s.jsx)(o.IIB,{type:"text",id:"description",name:"description",focusBorderColor:"gray.700",onChange:n,onBlur:t,value:a.description,isInvalid:i.description&&!!e.description,minW:"65%",w:"65%","data-testid":"input-description"}),(0,s.jsx)(o.ua7,{fontSize:"md",label:"An explanation of the type of organization and primary activity. For example “Acme Inc. is an e-commerce company that sells scarves.”",placement:"right",children:(0,s.jsx)(o.UOT,{boxSize:5,color:"gray.400"})})]})]})}),(0,s.jsx)(o.wpx,{type:"primary",htmlType:"submit",disabled:!a.name||!a.description,loading:l,"data-testid":"submit-btn",children:"Save and continue"})]})})},J=e=>{let{allColumns:t,selectedColumns:n,onChange:i}=e,a=(0,r.useMemo)(()=>{let e=new Map;return t.forEach(t=>e.set(t.name,!!n.find(e=>e.name===t.name))),e},[t,n]),l=()=>{a.forEach((e,t)=>a.set(t,!1)),i([])},c=e=>{var n;let s=null!==(n=a.get(e.name))&&void 0!==n&&n;a.set(e.name,!s),i(t.filter(e=>a.get(e.name)))};return(0,s.jsx)(o.v2r,{children:e=>{let{onClose:r}=e;return(0,s.jsxs)(s.Fragment,{children:[(0,s.jsx)(o.j2t,{as:o.wpx,icon:(0,s.jsx)(o.mCO,{}),fontWeight:"normal","data-testid":"column-dropdown",children:"Columns"}),(0,s.jsx)(o.qyq,{children:(0,s.jsxs)(o.xuv,{px:2,children:[(0,s.jsxs)(o.xuv,{display:"flex",justifyContent:"space-between",mb:2,children:[(0,s.jsx)(o.wpx,{size:"small",onClick:l,"data-testid":"column-clear-btn",children:"Clear"}),(0,s.jsx)(o.wpx,{type:"primary",size:"small",onClick:r,"data-testid":"column-done-btn",children:"Done"})]}),(0,s.jsx)(o.cOn,{colorScheme:"complimentary",children:(0,s.jsx)(o.Kqy,{children:t.map(e=>{let t=n.filter(t=>t.name===e.name).length>0;return(0,s.jsx)(o.XZJ,{id:e.name,_hover:{bg:"gray.100"},isChecked:t,onChange:()=>c(e),"data-testid":"checkbox-".concat(e.name),children:e.name},e.name)})})})]})})]})}})},Q=n(41498);let H=(e,t)=>t.split(".").reduce((e,t)=>e?e[t]:void 0,e),ee=e=>{let{system:t,attribute:n}=e;if("name"===n)return(0,s.jsx)("label",{htmlFor:"checkbox-".concat(t.fides_key),children:t.name});if("fidesctl_meta.resource_id"===n){var r,i;return(0,s.jsx)(o.xuv,{whiteSpace:"nowrap",overflow:"hidden",textOverflow:"ellipsis",title:(null===(r=t.fidesctl_meta)||void 0===r?void 0:r.resource_id)||"",children:null===(i=t.fidesctl_meta)||void 0===i?void 0:i.resource_id})}return(0,s.jsx)(s.Fragment,{children:H(t,n)})},et=e=>{let{allSystems:t,checked:n,onChange:r,columns:i,tableHeadProps:a}=e,l=e=>{n.indexOf(e)>=0?r(n.filter(t=>t.fides_key!==e.fides_key)):r([...n,e])},c=t.length===n.length;return 0===i.length?(0,s.jsx)(o.xvT,{children:"No columns selected to display"}):(0,s.jsxs)(o.iA_,{size:"sm",sx:{tableLayout:"fixed"},children:[(0,s.jsx)(o.hrZ,{...a,children:(0,s.jsxs)(o.Tr,{children:[(0,s.jsx)(o.Th,{width:"15px",children:(0,s.jsx)(o.XZJ,{colorScheme:"complimentary",title:"Select All",isChecked:c,onChange:e=>{e.target.checked?r(t):r([])},"data-testid":"select-all"})}),i.map(e=>(0,s.jsx)(o.Th,{children:e.name},e.attribute))]})}),(0,s.jsx)(o.p3B,{children:t.map(e=>(0,s.jsxs)(o.Tr,{children:[(0,s.jsx)(o.Td,{children:(0,s.jsx)(o.XZJ,{colorScheme:"complimentary",value:e.fides_key,isChecked:n.indexOf(e)>=0,onChange:()=>l(e),"data-testid":"checkbox-".concat(e.fides_key)})}),i.map(t=>(0,s.jsx)(o.Td,{children:(0,s.jsx)(ee,{system:e,attribute:t.attribute})},t.attribute))]},e.fides_key))})]})};var en=n(22153);let es=[{name:"Name",attribute:"name"},{name:"System type",attribute:"system_type"},{name:"Resource ID",attribute:"fidesctl_meta.resource_id"}];var er=()=>{let e=(0,i.C)(l.j4),t=(0,i.T)(),n=(0,c.useRouter)(),{systemOrDatamapRoute:a}=(0,Q.V)(),{isOpen:d,onOpen:u,onClose:h}=(0,o.qY0)(),[m]=(0,en.dB)(),[x,p]=(0,r.useState)(e),[g,y]=(0,r.useState)(es),{handleError:j}=(0,A.H)(),f=e=>{n.push(e).then(()=>{t((0,l.mc)())})},v=async()=>{let e=await m(x);return(0,_.D4)(e)?j(e.error):f(a)},b=()=>{t((0,l.sz)(2))},w=(0,s.jsxs)(o.xvT,{color:"gray.500",mb:3,children:["You’re registering ",x.length," of ",e.length," systems available. Do you want to continue with registration or cancel and register all systems now?"]});return(0,s.jsxs)(o.xuv,{maxW:"full",children:[(0,s.jsxs)(o.Kqy,{spacing:10,children:[(0,s.jsx)(o.X6q,{as:"h3",size:"lg","data-testid":"scan-results",children:"Scan results"}),0===e.length?(0,s.jsxs)(s.Fragment,{children:[(0,s.jsx)(o.xvT,{"data-testid":"no-results",children:"No results were found for your infrastructure scan."}),(0,s.jsx)(o.Ugi,{children:(0,s.jsx)(o.wpx,{onClick:b,"data-testid":"back-btn",children:"Back"})})]}):(0,s.jsxs)(s.Fragment,{children:[(0,s.jsxs)(o.xuv,{children:[(0,s.jsx)(o.xvT,{children:"Below are the results of your infrastructure scan. To continue, select the systems you would like registered in your data map and reports."}),(0,s.jsx)(o.xuv,{display:"flex",justifyContent:"end",children:(0,s.jsx)(J,{allColumns:es,selectedColumns:g,onChange:y})})]}),(0,s.jsx)(et,{allSystems:e,checked:x,onChange:p,columns:g}),(0,s.jsxs)(o.Ugi,{children:[(0,s.jsx)(o.wpx,{onClick:b,children:"Back"}),(0,s.jsx)(o.wpx,{onClick:()=>{e.length>x.length?u():v()},type:"primary",disabled:0===x.length,"data-testid":"register-btn",children:"Register selected systems"})]})]})]}),(0,s.jsx)(F.Z,{title:"Warning",message:w,handleConfirm:v,isOpen:d,onClose:h})]})},ei=()=>{let e=(0,i.C)(l.xx);return(0,s.jsx)(o.Kqy,{direction:["column","row"],bg:"white",children:(0,s.jsxs)(o.xuv,{display:"flex",justifyContent:"center",w:"100%",children:[1===e?(0,s.jsx)($,{}):null,2===e?(0,s.jsx)(w,{}):null,3===e?(0,s.jsx)(V,{}):null,4===e?(0,s.jsx)(o.xuv,{pr:10,children:(0,s.jsx)(er,{})}):null]})})},ea=()=>{let e=(0,i.T)();return(0,r.useEffect)(()=>{e((0,l.sz)(2))},[e]),(0,s.jsx)(a.Z,{title:"Config Wizard",children:(0,s.jsx)(ei,{})})}},41164:function(e,t,n){"use strict";n.d(t,{Bw:function(){return a},D4:function(){return r},Dy:function(){return o},XD:function(){return c},cz:function(){return d},hE:function(){return l},oK:function(){return i}});var s=n(76649);let r=e=>"error"in e,i=e=>(0,s.Ln)({status:"string"},e)&&"PARSING_ERROR"===e.status,a=e=>(0,s.Ln)({status:"number",data:{}},e),l=e=>(0,s.Ln)({detail:"string"},e),o=e=>(0,s.Ln)({detail:{error:"string",resource_type:"string",fides_key:"string"}},e),c=e=>(0,s.Ln)({detail:{error:"string",resource_type:"string",fides_key:"string"}},e),d=e=>(0,s.Ln)({detail:[{loc:["string","number"],msg:"string",type:"string"}]},e)},43073:function(e,t,n){"use strict";n.d(t,{Bw:function(){return s.Bw},D4:function(){return s.D4}});var s=n(41164)},76649:function(e,t,n){"use strict";n.d(t,{Ln:function(){return s}});let s=(e,t)=>i(e,t),r=Symbol("SOME"),i=(e,t)=>"string"==typeof e?e===typeof t:Array.isArray(e)?r in e?e.some(e=>i(e,t)):!!Array.isArray(t)&&(0===e.length||t.every(t=>e.some(e=>i(e,t)))):"object"==typeof t&&null!==t&&Object.entries(e).every(([e,n])=>i(n,t[e]));class a{static narrow(e){return new a(t=>s(e,t))}constructor(e){this.NF=void 0,this.NF=e}satisfied(e){return this.NF(e)}build(e){return e}and(e){let t=this.NF,n=e instanceof a?e.NF:e instanceof Function?e:t=>s(e,t);return new a(e=>t(e)&&n(e))}}new a(e=>!0)}},function(e){e.O(0,[2888,9774,179],function(){return e(e.s=74245)}),_N_E=e.O()}]);