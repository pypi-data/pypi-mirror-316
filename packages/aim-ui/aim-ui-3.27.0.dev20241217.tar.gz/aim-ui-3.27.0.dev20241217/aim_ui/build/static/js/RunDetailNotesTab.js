(this.webpackJsonpui_v2=this.webpackJsonpui_v2||[]).push([[18],{1040:function(e,t,n){"use strict";var a=n(7),i=n(0),o=n.n(i),c=n(99),s=n(786),l=n(5),r=n(1);var d=function(e){var t=e.when,n=e.message,i=void 0===n?"Changes you made may not be saved.":n,d=e.confirmBtnText,u=void 0===d?"Leave":d,j=o.a.useState(!1),b=Object(a.a)(j,2),f=b[0],v=b[1],m=o.a.useState(""),_=Object(a.a)(m,2),h=_[0],O=_[1],x=o.a.useState(!1),p=Object(a.a)(x,2),N=p[0],C=p[1],T=Object(c.h)();function g(e){return t?(null===e||void 0===e||e.preventDefault(),e&&(e.returnValue="Your changes is not saved. Do you still want to leave"),""):void 0}function y(){v(!1)}return o.a.useEffect((function(){return N&&(T.push(h),C(!1)),window.addEventListener("beforeunload",g),function(){window.removeEventListener("beforeunload",g)}}),[N,t]),Object(r.jsxs)(r.Fragment,{children:[Object(r.jsx)(c.a,{when:t,message:function(e){return!!N||(function(e){v(!0),O(e)}(e.pathname),!1)}}),Object(r.jsx)(s.a,{open:f,onCancel:y,onSubmit:function(){y(),h&&C(!0)},text:i,icon:Object(r.jsx)(l.f,{name:"warning-contained"}),statusType:"warning",confirmBtnText:u,title:"Are you sure"})]})};t.a=d},1383:function(e,t,n){"use strict";var a=n(7),i=n(0),o=n.n(i),c=n(1);t.a=function(e){var t=e.children,n=o.a.useRef(null),i=o.a.useState(!1),s=Object(a.a)(i,2),l=s[0],r=s[1];return o.a.useEffect((function(){if(l){var e=n.current.parentNode.parentNode.parentNode;"notes-toolbar-popover"!==e.id&&(e.id="notes-toolbar-popover")}else r(!0)}),[l]),Object(c.jsx)("div",{ref:n,children:t})}},1487:function(e,t,n){"use strict";var a=n(2),i=n(7),o=n(0),c=n.n(o),s=n(18),l=n.n(s),r=n(1030),d=n.n(r),u=n(67),j=n.n(u),b=n(228),f=n(291),v=n(5),m=n(794),_=n(406),h=n(1040),O=n(17),x=n(29),p=n(77),N=n(14),C=n(1435),T=n(1383),g=(n(1488),n(1));function y(e){var t,n=e.runHash,o=Object(b.a)(C.a),s=o.isLoading,r=o.noteData,u=o.notifyData,y=c.a.useState(""),w=Object(i.a)(y,2),D=w[0],E=w[1],M=c.a.useState(!0),R=Object(i.a)(M,2),S=R[0],B=R[1],k=c.a.useState(null),P=Object(i.a)(k,2),L=P[0],z=P[1],F=c.a.useRef(null);c.a.useEffect((function(){return C.a.initialize(n),N.a(O.a.runDetails.tabs.notes.tabView),function(){C.a.destroy()}}),[]),c.a.useEffect((function(){var e;F.current&&(E((null===r||void 0===r?void 0:r.id)?null===r||void 0===r?void 0:r.content:""),z(Object(a.a)(Object(a.a)({},null===(e=F.current)||void 0===e?void 0:e.theme()),x.c)))}),[r]);var I=c.a.useCallback((function(){B(!0),(null===r||void 0===r?void 0:r.id)?J():C.a.onNoteCreate(n,{content:F.current.value()})}),[null===r||void 0===r?void 0:r.id,n]),J=c.a.useCallback((function(){C.a.onNoteUpdate(n,{content:F.current.value()})}),[n]),U=c.a.useCallback((function(e){var t=D===e();S!==t&&B(t)}),[S,D]);return Object(g.jsxs)("section",{className:"RunDetailNotesTab",children:[Object(g.jsx)(h.a,{when:!S}),Object(g.jsxs)("div",{className:l()("RunDetailNotesTab__Editor",{isLoading:s}),children:[Object(g.jsxs)("div",{className:"RunDetailNotesTab__Editor__actionPanel",children:[Object(g.jsxs)("div",{className:"RunDetailNotesTab__Editor__actionPanel__info",children:[(null===r||void 0===r?void 0:r.created_at)&&Object(g.jsx)(f.a,{title:"Created at",children:Object(g.jsxs)("div",{className:"RunDetailNotesTab__Editor__actionPanel__info-field",children:[Object(g.jsx)(v.f,{name:"calendar"}),Object(g.jsx)(v.n,{tint:70,children:"".concat(j.a.utc(null===r||void 0===r?void 0:r.created_at).local().format(p.j))})]})}),(null===r||void 0===r?void 0:r.updated_at)&&Object(g.jsx)(f.a,{title:"Updated at",children:Object(g.jsxs)("div",{className:"RunDetailNotesTab__Editor__actionPanel__info-field",children:[Object(g.jsx)(v.f,{name:"time"}),Object(g.jsx)(v.n,{tint:70,children:"".concat(j.a.utc(null===r||void 0===r?void 0:r.updated_at).local().format(p.j))})]})})]}),Object(g.jsx)(f.a,{title:"Save Note",children:Object(g.jsx)("div",{children:Object(g.jsx)(v.c,{disabled:S||s,variant:"contained",size:"small",onClick:I,className:"RunDetailNotesTab__Editor__actionPanel__saveBtn",children:"Save"})})})]}),Object(g.jsx)(d.a,{ref:F,className:"RunDetailNotesTab__Editor__container",value:D,placeholder:"Leave your Note",theme:L||(null===(t=F.current)||void 0===t?void 0:t.theme()),disableExtensions:["table","image","container_notice"],tooltip:function(e){var t=e.children;return Object(g.jsx)(T.a,{children:t})},onChange:U}),s&&Object(g.jsx)("div",{className:"RunDetailNotesTab__spinnerWrapper",children:Object(g.jsx)(_.a,{})})]}),u.length>0&&Object(g.jsx)(m.a,{handleClose:C.a.onNoteNotificationDelete,data:u})]})}y.displayName="RunDetailNotesTab",t.a=c.a.memo(y)},1488:function(e,t,n){},1991:function(e,t,n){"use strict";n.r(t);var a=n(1487);t.default=a.a},786:function(e,t,n){"use strict";var a=n(0),i=n.n(a),o=n(732),c=n(5),s=n(227),l=(n(789),n(1));function r(e){return Object(l.jsx)(s.a,{children:Object(l.jsxs)(o.a,{open:e.open,onClose:e.onCancel,"aria-labelledby":"dialog-title","aria-describedby":"dialog-description",PaperProps:{elevation:10},className:"ConfirmModal ConfirmModal__".concat(e.statusType),children:[Object(l.jsxs)("div",{className:"ConfirmModal__Body",children:[Object(l.jsx)(c.c,{size:"small",className:"ConfirmModal__Close__Icon",color:"secondary",withOnlyIcon:!0,onClick:e.onCancel,children:Object(l.jsx)(c.f,{name:"close"})}),Object(l.jsxs)("div",{className:"ConfirmModal__Title__Container",children:[Object(l.jsx)("div",{className:"ConfirmModal__Icon",children:e.icon}),e.title&&Object(l.jsx)(c.n,{size:16,tint:100,component:"h4",weight:600,children:e.title})]}),Object(l.jsxs)("div",{children:[e.description&&Object(l.jsx)(c.n,{className:"ConfirmModal__description",weight:400,component:"p",id:"dialog-description",children:e.description}),Object(l.jsxs)("div",{children:[e.text&&Object(l.jsx)(c.n,{className:"ConfirmModal__text",weight:400,component:"p",size:14,id:"dialog-description",children:e.text||""}),e.children&&e.children]})]})]}),Object(l.jsxs)("div",{className:"ConfirmModal__Footer",children:[Object(l.jsx)(c.c,{onClick:e.onCancel,className:"ConfirmModal__CancelButton",children:e.cancelBtnText}),Object(l.jsx)(c.c,{onClick:e.onSubmit,color:"primary",variant:"contained",className:"ConfirmModal__ConfirmButton",autoFocus:!0,children:e.confirmBtnText})]})]})})}r.defaultProps={confirmBtnText:"Confirm",cancelBtnText:"Cancel",statusType:"info"},r.displayName="ConfirmModal",t.a=i.a.memo(r)},789:function(e,t,n){}}]);
//# sourceMappingURL=RunDetailNotesTab.js.map?version=2a39324bf82b8fae8f67