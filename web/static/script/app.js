angular
.module('Colorize', ['ngFileUpload'])
.filter('formatSize', function() {
    return function (size) {
        var unites = ["bytes", "KB", "MB", "GB", "TB", "PB"];
        var index = Math.floor(Math.log(size) / Math.log(1024));
        var unitSize = size / (Math.pow(1024, index));
        return unitSize.toFixed(1) + " " + unites[index];
    }
})
.controller('mainCtrl', ['$scope','$http','Upload', function($scope, $http, Upload) {

    var photoStatus = {
        Pending: "Pending",
        Uploading: "Uploading",
        Queued: "Queued",
        Processing: "Processing",
        Finished: "Finished",
        Error: "Error"
    };

    $scope.photos = [];

    $scope.addPhotos = function(files) {
        for(var i = 0; i < files.length; i++) {
            $scope.photos.push({
                file: files[i],
                status: photoStatus.Processing,
                //uploadProgress: 55,
                //queuePosition: 62,
                id: null
            });
        }
    };

    $scope.submitPhotos = function() {
        for(var i=0; i<$scope.photos.length; i++) {
            var photo = $scope.photos[i];
            if (photo.status === photoStatus.Pending) {
                uploadSingleFile(photo);
            }
        }
    };

    $scope.removePhoto = function(photo) {
        var index = $scope.photos.indexOf(photo);
        if(index >= 0) {
            $scope.photos.splice(index, 1);
        }
    };

    $scope.downloadPhoto = function(photo) {
        window.open("/output/"+photo.id);
    };


    function uploadSingleFile(photoToUpload) {
        photoToUpload.status = photoStatus.Uploading;
        photoToUpload.uploadProgress = 0;
        Upload.upload({
            url: '/upload',
            data: { 'photo': photoToUpload.file }
        }).then(function (response) {
            photoToUpload.id = response.data.id;
            checkStatus(photoToUpload);
        }, function (error) {
            photoToUpload.status = photoStatus.Error;
        }, function (evt) {
            photoToUpload.uploadProgress  = parseInt(100.0 * evt.loaded / evt.total);
        });
    }

    function checkStatus(photo) {
        $http.get("/status/"+photo.id).then(function(response) {
            console.log(response.data);
            photo.status = response.data.status;

            if (photo.status === photoStatus.Queued) {
                photo.queuePosition = response.data.queuePosition;
            }

            if (photo.status === photoStatus.Finished || photo.status === photoStatus.Error) {
                return;
            }

            setTimeout(function() { checkStatus(photo); },1000);
        });
    }
}]);
