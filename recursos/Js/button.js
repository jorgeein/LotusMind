function goToLink(link) {
    console.log(link.value)
    location.href = link.value
}

function toggle(){
    var video = document.querySelector(".video")
    video.classList.toggle("active")
    video.pause();
    video.currentTime = 0;
}