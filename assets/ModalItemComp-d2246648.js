import{C as o,A as r}from"./index-f554547e.js";function m(){const a=o(!1),e=o(!0),l=o(0),t=o(""),s=o(0);return{isModal:a,canModalCancel:e,taskId:l,errorId:s,openModal:function(n){l.value=n,a.value=!0,t.value=""},canControl:function(n){n?(r().setTransState(0),e.value=!0):(r().setTransState(1),e.value=!1)},modalClose:function(){a.value=!1,s.value=0,t.value=""},modalFormInput:t}}export{m};