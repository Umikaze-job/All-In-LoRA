import{d as a,A as i,q as n,_ as l,o as d,c as m,h as r,n as o,t as u}from"./index-32431f85.js";const p=a({props:{addClass:String,buttonName:String,buttonColorHover:{type:String,default:"bg-NormalButtonHover"},enable:{type:Boolean,default:!0}},data(){return{store:i()}},computed:{nowOpacity(){return this.store.getTransState==0&&this.enable?"opacity-100":"opacity-50"}},methods:{mouseEnterItem(e){if(this.store.getTransState==0&&this.enable){const t=e.target;t.children[0].classList.add("left-0"),t.children[0].classList.remove("right-0"),n({targets:t.children[0],width:"100%",easing:"easeOutExpo",duration:300})}},mouseLeaveItem(e){if(this.store.getTransState==0&&this.enable){const t=e.target;t.children[0].classList.remove("left-0"),t.children[0].classList.add("right-0"),n({targets:t.children[0],width:"0",easing:"easeOutExpo",duration:300})}},itemClick(e){this.store.getTransState==0&&this.enable&&this.$emit("click-item")}}}),c={class:o("border-winBorder py-1 px-6 rounded align-middle select-none")};function g(e,t,h,f,v,b){return d(),m("div",{onMouseenter:t[0]||(t[0]=(...s)=>e.mouseEnterItem&&e.mouseEnterItem(...s)),onMouseleave:t[1]||(t[1]=(...s)=>e.mouseLeaveItem&&e.mouseLeaveItem(...s)),class:o(`cursor-pointer relative rounded ${e.addClass} ${e.nowOpacity}`),onClick:t[2]||(t[2]=(...s)=>e.itemClick&&e.itemClick(...s))},[r("div",{class:o(`rounded w-0 h-full absolute top-0 left-0 z-[-1] ${e.buttonColorHover}`)},null,2),r("p",c,u(e.buttonName),1)],34)}const S=l(p,[["render",g]]);export{S as m};
