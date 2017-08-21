(function() {
    var index = 1;
    var size = null;
    var imageIndexIdNum = 0;
    var starIndex = 0;
    var feedback = {
        question: document.getElementById('pic_name'),
        contact: document.getElementById('contact'),
        imageList: document.getElementById('image-list'),
        submitBtn: document.getElementById('submit')
    };
    var url = 'http://111.231.62.167/wx/uploadImg';
    feedback.files = [];
    feedback.uploader = null;
    feedback.deviceInfo = null;
    mui.plusReady(function() {
        //设备信息，无需修改
        feedback.deviceInfo = {
            appid: plus.runtime.appid,
            imei: plus.device.imei, //设备标识
            images: feedback.files, //图片文件
            p: mui.os.android ? 'a' : 'i', //平台类型，i表示iOS平台，a表示Android平台。
            md: plus.device.model, //设备型号
            app_version: plus.runtime.version,
            plus_version: plus.runtime.innerVersion, //基座版本号
            os:  mui.os.version,
            net: ''+plus.networkinfo.getCurrentType()
        }
    });
    /**
     *提交成功之后，恢复表单项
     */
    feedback.clearForm = function() {
        feedback.question.value = '';
        feedback.contact.value = '';
        feedback.imageList.innerHTML = '';
        feedback.newPlaceholder();
        feedback.files = [];
        index = 0;
        size = 0;
        imageIndexIdNum = 0;
        starIndex = 0;
        //清除所有星标
        mui('.icons i').each(function (index,element) {
            if (element.classList.contains('mui-icon-star-filled')) {
                element.classList.add('mui-icon-star')
                element.classList.remove('mui-icon-star-filled')
            }
        })
    };
    feedback.getFileInputArray = function() {
        return [].slice.call(feedback.imageList.querySelectorAll('.file'));
    };
    feedback.addFile = function(path) {
        feedback.files.push({name:"images"+index,path:path,id:"img-"+index});
        index++;
    };
    /**
     * 初始化图片域占位
     */
    feedback.newPlaceholder = function() {
        var fileInputArray = feedback.getFileInputArray();
        if (fileInputArray &&
            fileInputArray.length > 0 &&
            fileInputArray[fileInputArray.length - 1].parentNode.classList.contains('space')) {
            return;
        };
        imageIndexIdNum++;
        var placeholder = document.createElement('div');
        placeholder.setAttribute('class', 'image-item space');
        var up = document.createElement("div");
        up.setAttribute('class','image-up')

        var fileInput = document.createElement('div');
        fileInput.setAttribute('class', 'file');
        fileInput.setAttribute('id', 'image-' + imageIndexIdNum);
        fileInput.addEventListener('tap', function(event) {
            var self = this;
            var index = (this.id).substr(-1);

            wx.chooseImage({
                count: 1, // 默认9
                sizeType: ['original', 'compressed'], // 可以指定是原图还是压缩图，默认二者都有
                sourceType: ['album', 'camera'], // 可以指定来源是相册还是相机，默认二者都有
                success: function (res) {
                    var localIds = res.localIds; // 返回选定照片的本地ID列表，localId可以作为img标签的src属性显示图片
					var imgSrc = localIds[0];
					placeholder.style.backgroundImage = "url("+imgSrc+")";
					if (!self.parentNode.classList.contains('space')) { //已有图片
						feedback.files.splice(index-1,1,{name:"images"+index,path:imgSrc});
					} else { //加号
						placeholder.classList.remove('space');
						feedback.addFile(imgSrc);
					}
					up.classList.remove('image-up');
                }
            });
        }, false);
        placeholder.appendChild(up);
        placeholder.appendChild(fileInput);
        feedback.imageList.appendChild(placeholder);
    };
    feedback.newPlaceholder();
    feedback.submitBtn.addEventListener('tap', function(event) {
        if (feedback.contact.value == '') {
            return mui.toast('请填写画作名称');
        }
        if (feedback.question.value.length > 200 || feedback.contact.value.length > 200) {
            return mui.toast('信息超长,请重新填写~')
        }
        feedback.send(mui.extend({}, feedback.deviceInfo, {
            picname: feedback.question.value,
            content: feedback.contact.value,
            images: feedback.files
        }))
    }, false)
    feedback.send = function(content) {
        //添加上传数据
		var post_data = "";
        mui.each(content, function(index, element) {
            if (index !== 'images') {
            	post_data+='"'+index+'":"'+element+'"&';
            }
        });

        var openId = $('#openId').val();
        post_data+='"openId":"'+openId+'"&';

        var file = feedback.files[0];
        //调用微信js上传图片
        wx.uploadImage({
            localId: file.path, // 需要上传的图片的本地ID，由chooseImage接口获得
            isShowProgressTips: 1, // 默认为1，显示进度提示
            success: function (res) {
                var serverId = res.serverId; // 返回图片的服务器端ID
                post_data+='"mediaId":"'+serverId+'"';
                $.post(url, post_data, function () {
                    mui.alert("感谢你的上传，点击确定关闭","画作分享","确定",function () {
                        feedback.clearForm();
                        mui.back();
                    });
                })
            },
            error:function (res) {
              alert(res);
            }
        });
    };
})();