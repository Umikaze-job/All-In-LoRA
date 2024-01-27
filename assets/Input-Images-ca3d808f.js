import{d as T,m as E,b as A,a as _,A as j,g as M,_ as P,r as l,o as n,c as h,e as m,w as d,F as $,f as R,t as g,h as o,k as r,j as p,K as F,i as H,n as O,p as U}from"./index-09c46877.js";import{T as W}from"./template01-92276447.js";import{D as V}from"./Dropable_Image02-ec89c5f5.js";import{m as Z}from"./mini-Button01-fadaf757.js";import{m as K}from"./mini-Button02-28aa58d0.js";import{I as q}from"./Image_window01-109ac729.js";import{I as z}from"./ImageItemComp-5cb7bdd1.js";import{m as G}from"./ModalItemComp-450d0411.js";/* empty css                       */const J=T({components:{"base-tem":W,"mini-button":Z,"image-window":q,"mini-button02":K,"image-item":V,"modal-base":E,"modal-window":A,"modal-button":_},setup(e,t){const{selecting_id:i,isMultipleSelect:s,ImageDataSet:u,selectImageItemID:f,selectingImageDataSet:c,clickAllItems:v,ImageWindowPreview:C,ImageWindowThumbnailPreview:k,getFileNameFromUrl:y,PreviewImageSelectLeft:w,PreviewImageSelectRight:I}=z(),{isModal:D,canModalCancel:a,taskId:b,errorId:S,openModal:N,canControl:B,modalClose:L}=G();return{selecting_id:i,isMultipleSelect:s,ImageDataSet:u,selectImageItemID:f,selectingImageDataSet:c,clickAllItems:v,ImageWindowPreview:C,ImageWindowThumbnailPreview:k,isModal:D,canModalCancel:a,taskId:b,errorId:S,openModal:N,canControl:B,modalClose:L,getFileNameFromUrl:y,PreviewImageSelectLeft:w,PreviewImageSelectRight:I}},computed:{getDragZone(){return this.isDragging?"border-rose-400 border-dashed":"border-white border-solid"}},data(){return{store:j(),previewImageOpen:!1,modalThumbnail:"",isDragging:!1}},async created(){this.selectingImageDataSet=[],await this.getImageList()},watch:{isModal:function(e){e==!1&&(this.modalThumbnail="")}},methods:{inputThumbnail(e){e.target.files!=null&&e.target.files.length!=0?this.modalThumbnail=URL.createObjectURL(e.target.files[0]):this.modalThumbnail=""},async ApplyModalButtonClick(e){if(e==0&&this.taskId==0){const t=this.$refs.thumbnail;if(t.files[0]!=null)await this.inputImages([t.files[0]]),this.modalClose();else{this.errorId=1;return}}else if(e==0&&this.taskId==1){let t=!1;this.canControl(!1);for(const i of this.selecting_id){const s=await this.axios.post(M()+"/api/processing-images/delete-input-images",{fileName:this.selectingImageDataSet[i].image_url.split("\\").pop(),folderName:this.store.getSelectingFolderName.id});if(s.data.error!=null){t=!0,this.store.setErrorMessage(s.data.error);break}}t==!1&&await this.getImageList(),this.selecting_id=[-1],this.canControl(!0),this.modalClose()}else e==1&&this.modalClose()},async getImageList(){const e=await this.axios.post(M()+"/api/processing-images/input-images",{folderName:this.store.getSelectingFolderName.id});if(e.data.error==null){const t=e.data;this.selectingImageDataSet=t.data_paths.map((i,s)=>({image_url:i,thumbnail_path:e.data.thumbnail_path[s],file_name:t.displayed_name[s],tags:[]}))}else this.store.setErrorMessage(e.data.error)},async inputImages(e){let t=!1;if(this.canControl(!1),e.length>0)for(let i=0;i<e.length;i++){const s=e[i],u=new FormData;u.append("file",s),u.append("folderName",this.store.getSelectingFolderName.id);const f=await this.axios.post(M()+"/api/processing-images/set-input-images",u,{headers:{"Content-Type":"multipart/form-data"}});if(f.data.error!=null){this.store.setErrorMessage(f.data.error),t=!0;break}}t==!1&&await this.getImageList(),this.canControl(!0)},handleDragEnter(){this.isDragging=!0},handleDragLeave(){this.isDragging=!1},async dropHandler(e){e.preventDefault(),this.isDragging=!1;const t=e.dataTransfer.files;t.length!=0&&t[0]!=null&&(this.isModal=!0,await this.inputImages(t),this.modalClose())},dragOverHandler(e){e.preventDefault()}}}),Q={class:"flex flex-row text-center text-lg text-white font-Raleway"},X={class:"basis-1/3 flex flex-row justify-start"},Y={class:"basis-1/3 flex flex-row justify-end items-center gap-2"},x={class:"basis-1/3 flex flex-row justify-end gap-2"},ee={key:0,id:"contentstyle02",class:"grid 2xl:grid-cols-7 xl:grid-cols-6 lg:grid-cols-5 md:grid-cols-4 gap-4 m-3 pr-3 text-white font-Raleway overflow-y-auto"},te={key:1,class:"flex flex-row justify-center items-center min-h-[200px]"},ae={class:"text-white font-Raleway text-xl h-full pointer-events-none"},ne={class:"text-center text-xl underline decoration-myUnderLine01 py-3"},oe={class:"text-center text-lg"},ie={key:0,class:"text-center text-lg text-red-400"},se={key:1,class:"h-[200px] flex flex-row justify-center items-center"},le=["src"],re={class:"text-center text-xl underline decoration-myUnderLine01 py-3"},me={class:"text-center text-lg"},de=o("p",{class:"text-center text-xl underline decoration-myUnderLine01 py-8"},"Loading...",-1);function ge(e,t,i,s,u,f){const c=l("mini-button"),v=l("mini-button02"),C=l("image-window"),k=l("image-item"),y=l("base-tem"),w=l("modal-button"),I=l("modal-window"),D=l("modal-base");return n(),h($,null,[m(y,null,{maintitle:d(()=>[R(g(e.$t("topbar.EditImages.main")),1)]),buttonContents:d(()=>[o("div",Q,[o("div",X,[m(c,{onClick:t[0]||(t[0]=a=>e.openModal(0)),buttonName:e.$t("ImageInput.miniButton.InputImage")},null,8,["buttonName"])]),o("div",Y,[m(c,{onClickItem:e.clickAllItems,"button-name":e.$t("ImageInput.miniButton.AllSelect")},null,8,["onClickItem","button-name"]),m(v,{onClickItem:t[1]||(t[1]=a=>e.isMultipleSelect=!e.isMultipleSelect),"is-clicked":e.isMultipleSelect,"button-name":e.$t("ImageInput.miniButton.MultipleSelect")},null,8,["is-clicked","button-name"])]),o("div",x,[e.selecting_id[0]!=-1&&e.selecting_id.length!=0?(n(),r(c,{key:0,onClick:t[2]||(t[2]=a=>e.previewImageOpen=!0),buttonName:e.$t("ImageInput.miniButton.Preview")},null,8,["buttonName"])):p("",!0),e.selecting_id[0]!=-1&&e.selecting_id.length!=0?(n(),r(c,{key:1,onClick:t[3]||(t[3]=a=>e.openModal(1)),buttonName:e.$t("ImageInput.miniButton.Delete"),"button-color-hover":"bg-DeleteColor"},null,8,["buttonName"])):p("",!0)])])]),mainContents:d(()=>[(n(),r(F,null,[e.previewImageOpen?(n(),r(C,{key:0,onClickLeft:e.PreviewImageSelectLeft,onClickRight:e.PreviewImageSelectRight,onImageWindowCancel:t[4]||(t[4]=a=>e.previewImageOpen=!1),imgsrc:e.ImageWindowPreview,"thumbnail-src":e.ImageWindowThumbnailPreview},null,8,["onClickLeft","onClickRight","imgsrc","thumbnail-src"])):p("",!0)],1024)),o("div",{class:O(`border-winBorder ${e.getDragZone} rounded-lg min-h-[200px] transition-all`),onDrop:t[5]||(t[5]=(...a)=>e.dropHandler&&e.dropHandler(...a)),onDragenter:t[6]||(t[6]=(...a)=>e.handleDragEnter&&e.handleDragEnter(...a)),onDragleave:t[7]||(t[7]=(...a)=>e.handleDragLeave&&e.handleDragLeave(...a)),onDragover:t[8]||(t[8]=U((...a)=>e.dragOverHandler&&e.dragOverHandler(...a),["prevent"]))},[e.selectingImageDataSet.length!=0?(n(),h("div",ee,[(n(!0),h($,null,H(e.selectingImageDataSet,(a,b)=>(n(),r(k,{key:b,"image-path":a.thumbnail_path,id:b,"selected-id":e.selecting_id,onClick:S=>e.selectImageItemID(b),"file-name":a.file_name},null,8,["image-path","id","selected-id","onClick","file-name"]))),128))])):(n(),h("div",te,[o("p",ae,g(e.$t("ImageInput.dropZone")),1)]))],34)]),_:1}),m(D,{"is-window":e.isModal,onModalCancel:t[10]||(t[10]=a=>e.isModal=!1),"can-background-cancel":e.canModalCancel},{default:d(()=>[e.store.getTransState==0&&e.taskId==0?(n(),r(I,{key:0},{default:d(()=>[o("p",ne,g(e.$t("ImageInput.miniButton.InputImage")),1),o("p",oe,g(e.$t("ImageInput.modalMessage.InputImages")),1),e.errorId==1?(n(),h("p",ie,g(e.$t("ImageInput.modalErrorMessage.NoImage")),1)):p("",!0),o("input",{onChange:t[9]||(t[9]=(...a)=>e.inputThumbnail&&e.inputThumbnail(...a)),class:"mx-auto text-center",type:"file",ref:"thumbnail",accept:".jpg, .jpeg, .png, .webp, .bmp"},null,544),e.modalThumbnail!=""?(n(),h("div",se,[o("img",{src:e.modalThumbnail,class:"max-h-full"},null,8,le)])):p("",!0),m(w,{onClickItem:e.ApplyModalButtonClick,"button-porps":[{name:"Input image",hoverColor:"hover:bg-ApplyColor"},{name:"Cancel",hoverColor:"hover:bg-NormalButtonHover"}]},null,8,["onClickItem"])]),_:1})):p("",!0),e.store.getTransState==0&&e.taskId==1?(n(),r(I,{key:1},{default:d(()=>[o("p",re,g(e.$t("ImageInput.modalMessage.deleteImage.title")),1),o("p",me,g(e.$tc("ImageInput.modalMessage.deleteImage.contents",e.selecting_id)),1),m(w,{onClickItem:e.ApplyModalButtonClick,"button-porps":[{name:"Delete",hoverColor:"hover:bg-DeleteColor"},{name:"Cancel",hoverColor:"hover:bg-NormalButtonHover"}]},null,8,["onClickItem"])]),_:1})):e.store.getTransState==1?(n(),r(I,{key:2},{default:d(()=>[de]),_:1})):p("",!0)]),_:1},8,["is-window","can-background-cancel"])],64)}const Ce=P(J,[["render",ge]]);export{Ce as default};
