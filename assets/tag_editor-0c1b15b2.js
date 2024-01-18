import{a as h}from"./tag_name-6410ff4f.js";import{d as B,_ as $,o as r,c as m,h as i,t as g,n as N,j as M,A as R,g as S,r as p,k as f,w as v,f as A,e as u,K as U,i as T,F as _,l as C,x as k}from"./index-32431f85.js";import{T as j}from"./template01-64c007ef.js";import{m as P}from"./mini-Button01-f793155e.js";import{m as L}from"./mini-Button02-6365ff8a.js";import{r as F}from"./row-Buttons02-be6ce8a5.js";import{I as W,D as V}from"./ImageItemComp-5179b1cf.js";import{I as z}from"./Image_window01-cdfc2eb6.js";const K=B({props:{count:Number,name:String,type:{type:Number,default:0},isSelected:{type:Boolean,default:!1}},computed:{buttonColor(){return this.isSelected?"bg-red-950":"bg-NormalButtonColor"},hoverColor(){return this.isSelected?" hover:bg-red-800":" hover:bg-neutral-700"}}}),q={class:"my-auto"},G=i("div",{class:"w-[1px] h-[90%] my-auto bg-white"},null,-1),H={class:"my-auto"},J={key:1,class:"text-white font-Raleway gap-3 bg-NormalButtonColor px-3 h-[32px] rounded-lg select-none text-sm"},O={class:"my-auto leading-8"};function Q(e,t,o,a,l,n){return e.type==0?(r(),m("div",{key:0,class:N("flex flex-row text-white font-Raleway gap-3 transition-colors px-3 h-[32px] rounded-lg select-none text-sm cursor-pointer "+e.buttonColor+e.hoverColor)},[i("p",q,g(e.count),1),G,i("p",H,g(e.name),1)],2)):e.type==1?(r(),m("div",J,[i("p",O,g(e.name),1)])):M("",!0)}const X=$(K,[["render",Q]]),Y=B({setup(e,t){const{selecting_id:o,isMultipleSelect:a,ImageDataSet:l,ImageFolderID:n,selectImageItemID:d,selectingImageDataSet:w,clickAllItems:b,ImageWindowPreview:x,ImageWindowThumbnailPreview:E,ImageFolderRowButtonClick:I,PreviewImageSelectLeft:y,PreviewImageSelectRight:s}=W();return{selecting_id:o,isMultipleSelect:a,ImageDataSet:l,ImageFolderID:n,selectImageItemID:d,selectingImageDataSet:w,clickAllItems:b,ImageWindowPreview:x,ImageWindowThumbnailPreview:E,ImageFolderRowButtonClick:I,PreviewImageSelectLeft:y,PreviewImageSelectRight:s}},components:{"base-tem":j,"mini-btn01":P,"mini-btn02":L,"row-btn02":F,"image-item":V,"tag-button":X,"image-window":z},data(){return{nowMultiImageEditId:0,MultiImageEditTags:{add:"",replace:{beforetags:[],aftertags:""},delete:[]},store:R(),isImageWindow:!1}},computed:{NowMultiImageEditTags(){return this.nowMultiImageEditId==0?[]:this.nowMultiImageEditId==1?this.MultiImageEditTags.replace.beforetags:this.MultiImageEditTags.delete},getSelectedItem(){return this.selecting_id[0]!=-1&&this.selecting_id.length==1?this.selectingImageDataSet[this.selecting_id[0]]:{}},getAggregationTags(){let e=[];this.selecting_id.forEach((a,l)=>{let n=this.selectingImageDataSet[a].imgtag.split(",");n=n.map(d=>d.trim()),e=e.concat(n)});const t=[...new Set(e)];let o=[];return t.forEach((a,l)=>{const n=e.reduce(function(d,w){return w===a?d+1:d},0);o.push({name:a,count:n})}),o=o.filter(a=>a.name!=""),o=o.sort((a,l)=>a.name.localeCompare(l.name)),o}},async beforeUnmount(){await this.axios.post(S()+"/api/make-textfile/edit_tag/write",{folderName:this.store.getSelectingFolderName,base:this.ImageDataSet.base,after:this.ImageDataSet.after})},async mounted(){const e=await this.axios.post(S()+"/api/make-textfile/edit_tag/getdata",{folderName:this.store.getSelectingFolderName});this.ImageDataSet.base=[],e.data.base.forEach((t,o)=>{const a=[];t.tag.join(",")!=null&&t.tag.join(",")!=""&&a.push({tagname:h.alreadyTag.name,tagcolor:h.alreadyTag.color}),this.ImageDataSet.base.push({image_url:t.image_path,thumbnail_path:t.thumbnail_path,file_name:t.file_name,tags:a,imgtag:t.tag.join(",")})}),this.ImageDataSet.after=[],e.data.after.forEach((t,o)=>{const a=[];t.tag.join(",")!=null&&t.tag.join(",")!=""&&a.push({tagname:h.alreadyTag.name,tagcolor:h.alreadyTag.color}),this.ImageDataSet.after.push({image_url:t.image_path,thumbnail_path:t.thumbnail_path,file_name:t.file_name,tags:a,imgtag:t.tag.join(",")})})},methods:{ImageTagUpdate(e){e.imgtag!=""?e.tags=[{tagname:h.alreadyTag.name,tagcolor:h.alreadyTag.color}]:e.tags=[]},MultiImageEditClick(e){this.nowMultiImageEditId=e},MultipleButtonClick(e){this.isMultipleSelect=!this.isMultipleSelect},tagButtonClick(e){this.nowMultiImageEditId==1?this.MultiImageEditTags.replace.beforetags.findIndex(t=>t==e)==-1?(this.MultiImageEditTags.replace.beforetags.push(e),this.MultiImageEditTags.replace.beforetags=[...new Set(this.MultiImageEditTags.replace.beforetags)]):this.MultiImageEditTags.replace.beforetags=this.MultiImageEditTags.replace.beforetags.filter(t=>t!=e):this.nowMultiImageEditId==2&&(this.MultiImageEditTags.delete.findIndex(t=>t==e)==-1?(this.MultiImageEditTags.delete.push(e),this.MultiImageEditTags.delete=[...new Set(this.MultiImageEditTags.delete)]):this.MultiImageEditTags.delete=this.MultiImageEditTags.delete.filter(t=>t!=e))},MultiImageEditAddClick(){this.selectingImageDataSet.filter((t,o)=>this.selecting_id.includes(o)).forEach((t,o)=>{var n;const a=this.MultiImageEditTags.add.split(",");let l=(n=t.imgtag)==null?void 0:n.split(",");l=l==null?void 0:l.concat(a),l=[...new Set(l)],l=l.map(d=>d.trim()),l=l.filter(d=>d!=null&&d!==""),t.imgtag=this.tagArrToStr(l),this.ImageTagUpdate(t)}),this.MultiImageEditTags.add=""},MultiImageEditReplaceClick(){this.selectingImageDataSet.filter((t,o)=>this.selecting_id.includes(o)).forEach((t,o)=>{let a=t.imgtag.split(",");a=a.filter(n=>!this.MultiImageEditTags.replace.beforetags.includes(n));const l=this.MultiImageEditTags.replace.aftertags.split(",");a=a.concat(l),a=[...new Set(a)],a=a.map(n=>n.trim()),a=a.filter(n=>n!=null&&n!==""),t.imgtag=this.tagArrToStr(a),this.ImageTagUpdate(t)}),this.MultiImageEditTags.replace={beforetags:[],aftertags:""}},MultiImageEditDeleteClick(){const e=this.selectingImageDataSet.filter((t,o)=>this.selecting_id.includes(o));e.forEach((t,o)=>{let a=t.imgtag.split(",");a=a.map(l=>l.trim()),a=a.filter(l=>!this.MultiImageEditTags.delete.includes(l)),a=a.filter(l=>l!=null&&l!==""),e[o].imgtag=this.tagArrToStr(a),this.ImageTagUpdate(t)}),this.MultiImageEditTags.delete=[]},tagArrToStr(e){return e.length==0?"":e.length==1?e[0]:e.join(",")}}}),Z={class:"flex flex-row text-center text-lg text-white font-Raleway gap-2 mt-6"},ee={class:"flex flex-row basis-1/2"},te={class:"basis-2/3 justify-start flex flex-row gap-2"},ae={class:"basis-1/3 justify-end flex flex-row"},ie={class:"flex flex-row justify-end basis-1/2"},le={class:"flex flex-row gap-2 mt-3"},se={class:"border-winBorder basis-3/5 border-white min-h-[100px] rounded-lg grid grid-cols-4 gap-2 overflow-y-auto max-h-[600px] p-2 text-white font-Raleway"},oe={class:"border-winBorder basis-2/5 border-white min-h-[100px] rounded-lg overflow-y-auto max-h-[600px]"},ne={key:0,class:"flex flex-col gap-2 p-3"},re={class:"text-center text-white font-Raleway text-lg"},de={key:1,class:"flex flex-col gap-2 p-3"},ge={class:"relative mt-5"},me={class:"bg-NormalButtonColor w-full h-[200px] mx-auto border-winBorder border-white rounded-lg"},ue=i("div",{class:"absolute h-[42px] left-[24px] top-[-21px] bg-NormalButtonColor border-white border-winBorder rounded-lg"},[i("p",{class:"text-white font-Raleway text-center py-[6px] px-[12px]"},"Tags")],-1),ce={key:2,class:"flex flex-col gap-6 p-3"},pe={class:"flex flex-col gap-2"},fe={class:"text-white font-Raleway text-center underline decoration-myUnderLine01 text-lg"},he={class:"flex flex-row flex-wrap gap-2"},we={key:0,class:"flex flex-col gap-4"},Ie={class:"text-white font-Raleway px-2 underline decoration-myUnderLine01 text-lg"},be={class:"flex flex-col gap-1"},Te={class:"px-3 text-white font-Raleway"},_e={class:"flex flex-row gap-1 text-white font-Raleway"},xe={key:1,class:"flex flex-col gap-4"},Ee={class:"text-white font-Raleway px-2 underline decoration-myUnderLine01 text-lg"},ye={class:"flex flex-col gap-1"},ve={class:"px-3 text-white font-Raleway"},Ce={class:"basis-5/6 border-winBorder border-white rounded flex flex-row flex-wrap gap-2 p-3"},ke={class:"flex flex-col gap-1"},Me={class:"px-3 text-white font-Raleway"},Se={class:"flex flex-row gap-1 text-white font-Raleway"},Be={key:2,class:"flex flex-col gap-4"},$e={class:"text-white font-Raleway px-2 underline decoration-myUnderLine01 text-lg"},De={class:"flex flex-col gap-1"},Ne={class:"px-3 text-white font-Raleway"},Re={class:"flex flex-row gap-1 text-white font-Raleway"},Ae={class:"basis-5/6 border-winBorder border-white rounded flex flex-row flex-wrap gap-2 p-3"};function Ue(e,t,o,a,l,n){const d=p("mini-btn01"),w=p("mini-btn02"),b=p("row-btn02"),x=p("image-window"),E=p("image-item"),I=p("tag-button"),y=p("base-tem");return r(),f(y,null,{maintitle:v(()=>[A(g(e.$t("topbar.MakeTextFile.TagEditor")),1)]),buttonContents:v(()=>[i("div",Z,[i("div",ee,[i("div",te,[u(d,{buttonName:e.$t("TagEditor.miniButton.AllSelect"),addClass:"",onClick:e.clickAllItems},null,8,["buttonName","onClick"]),u(w,{buttonName:e.$t("TagEditor.miniButton.MultipleSelect"),isClicked:e.isMultipleSelect,onClickItem:e.MultipleButtonClick},null,8,["buttonName","isClicked","onClickItem"])]),i("div",ae,[u(d,{buttonName:e.$t("TagEditor.miniButton.Preview"),enable:e.selecting_id[0]!=-1&&e.selecting_id.length!=0,onClickItem:t[0]||(t[0]=s=>e.isImageWindow=!0)},null,8,["buttonName","enable"])])]),i("div",ie,[u(b,{onClickItem:e.ImageFolderRowButtonClick,nowId:e.ImageFolderID,subItems:[e.$t("TagEditor.rowButton.base"),e.$t("TagEditor.rowButton.after")],addClass:""},null,8,["onClickItem","nowId","subItems"])])])]),mainContents:v(()=>[(r(),f(U,null,[e.isImageWindow?(r(),f(x,{key:0,"thumbnail-src":e.ImageWindowThumbnailPreview,imgsrc:e.ImageWindowPreview,onImageWindowCancel:t[1]||(t[1]=s=>e.isImageWindow=!1),onClickLeft:e.PreviewImageSelectLeft,onClickRight:e.PreviewImageSelectRight},null,8,["thumbnail-src","imgsrc","onClickLeft","onClickRight"])):M("",!0)],1024)),i("div",le,[i("div",se,[(r(!0),m(_,null,T(e.selectingImageDataSet,(s,c)=>(r(),f(E,{key:c,onClick:D=>e.selectImageItemID(c),"selected-id":e.selecting_id,id:c,imagePath:s.thumbnail_path,"file-name":s.file_name,"tag-data":s.tags},null,8,["onClick","selected-id","id","imagePath","file-name","tag-data"]))),128))]),i("div",oe,[e.selecting_id[0]==-1||e.selecting_id.length==0?(r(),m("div",ne,[i("p",re,g(e.$t("TagEditor.NoImages")),1)])):e.selecting_id[0]!=-1&&e.selecting_id.length==1?(r(),m("div",de,[i("div",ge,[i("div",me,[C(i("textarea",{class:"pt-[32px] px-3 bg-transparent text-white font-Raleway border-none outline-none focus:ring-transparent resize-none whitespace-break-spaces w-full h-full rounded-lg",onInput:t[2]||(t[2]=s=>e.ImageTagUpdate(e.getSelectedItem)),"onUpdate:modelValue":t[3]||(t[3]=s=>e.getSelectedItem.imgtag=s)},null,544),[[k,e.getSelectedItem.imgtag]])]),ue])])):(r(),m("div",ce,[i("div",pe,[i("p",fe,g(e.$t("TagEditor.AggTags")),1),i("div",he,[(r(!0),m(_,null,T(e.getAggregationTags,(s,c)=>(r(),f(I,{key:c,"is-selected":e.NowMultiImageEditTags.includes(s.name),count:s.count,name:s.name,onClick:D=>e.tagButtonClick(s.name)},null,8,["is-selected","count","name","onClick"]))),128))])]),u(b,{"sub-items":[e.$t("TagEditor.rowButton.addTags"),e.$t("TagEditor.rowButton.replaceTags"),e.$t("TagEditor.rowButton.deleteTags")],onClickItem:e.MultiImageEditClick,"now-id":e.nowMultiImageEditId,"add-class":"h-[32px]","add-text-class":"text-lg"},null,8,["sub-items","onClickItem","now-id"]),e.nowMultiImageEditId==0?(r(),m("div",we,[i("p",Ie,g(e.$t("TagEditor.rowButton.addTags")),1),i("div",be,[i("p",Te,g(e.$t("TagEditor.form.addTags")),1),i("div",_e,[C(i("input",{type:"text","onUpdate:modelValue":t[4]||(t[4]=s=>e.MultiImageEditTags.add=s),class:"rounded-sm bg-NormalButtonColor border-winBorder border-white basis-5/6 text-sm transition-colors"},null,512),[[k,e.MultiImageEditTags.add]]),u(d,{"add-class":"text-center basis-1/6 h-full my-auto","button-name":"add",onClick:e.MultiImageEditAddClick},null,8,["onClick"])])])])):e.nowMultiImageEditId==1?(r(),m("div",xe,[i("p",Ee,g(e.$t("TagEditor.rowButton.replaceTags")),1),i("div",ye,[i("p",ve,g(e.$t("TagEditor.form.beforeTags")),1),i("div",Ce,[(r(!0),m(_,null,T(e.MultiImageEditTags.replace.beforetags,(s,c)=>(r(),f(I,{type:1,name:s},null,8,["name"]))),256))])]),i("div",ke,[i("p",Me,g(e.$t("TagEditor.form.afterTags")),1),i("div",Se,[C(i("input",{type:"text","onUpdate:modelValue":t[5]||(t[5]=s=>e.MultiImageEditTags.replace.aftertags=s),class:"rounded-sm bg-NormalButtonColor border-winBorder border-white basis-5/6 text-sm transition-colors"},null,512),[[k,e.MultiImageEditTags.replace.aftertags]]),u(d,{"add-class":"text-center basis-1/6 h-full my-auto","button-name":"replace",onClick:e.MultiImageEditReplaceClick},null,8,["onClick"])])])])):e.nowMultiImageEditId==2?(r(),m("div",Be,[i("p",$e,g(e.$t("TagEditor.rowButton.deleteTags")),1),i("div",De,[i("p",Ne,g(e.$t("TagEditor.form.deleteTags")),1),i("div",Re,[i("div",Ae,[(r(!0),m(_,null,T(e.MultiImageEditTags.delete,(s,c)=>(r(),f(I,{type:1,name:s},null,8,["name"]))),256))]),u(d,{onClick:e.MultiImageEditDeleteClick,"add-class":"text-center basis-1/6 h-full my-auto","button-name":"delete","button-color-hover":"bg-DeleteColor"},null,8,["onClick"])])])])):M("",!0)]))])])]),_:1})}const qe=$(Y,[["render",Ue]]);export{qe as default};
