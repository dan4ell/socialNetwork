aboutLink = document.getElementById('aboutLink');
cardBody = document.getElementById('defaultProfile')
aboutLink.addEventListener('click', function(event){
event.preventDefault();
var computedStyle = window.getComputedStyle(cardBody);
var borderValue = computedStyle.getPropertyValue('border')
var shadowValue = computedStyle.getPropertyValue('box-shadow')
cardBody.style.boxShadow = '0 0 35px #303e47'
setTimeout(function(){
cardBody.style.border = "0px none rgb(33, 37, 41)"
cardBody.style.boxShadow = 'none'
}, 1000)
})

// edit profile

editProfileDiv = document.getElementById('editProfileDiv');
defaultProfile = document.getElementById('defaultProfile');
editProfileButton = document.getElementById('editProfileBtn');
defaultProfileButton = document.getElementById('defaultProfileBtn');
saveProfileButton = document.getElementById('save');

editProfileBtn.addEventListener('click', function(){
defaultProfile.style.display = 'none';
editProfileDiv.style.display = 'block';
})
defaultProfileButton.addEventListener('click', function(){
defaultProfile.style.display = 'block';
editProfileDiv.style.display = 'none';
})

// status correct

function status(){
    var statusSpan = document.getElementById('status');
    var statusContent = statusSpan.textContent;
    var cropContent = statusContent.substring(0, 50)
    var fullContent = statusContent
    var link = document.createElement('a')
    link.textContent = '...'
    link.href = '#'
    link.setAttribute('class', 'status-link')
    if(statusContent.length > 50){
            link.onclick = function(){
                    statusSpan.textContent = fullContent
                }
        }
    statusSpan.textContent = cropContent
    statusSpan.appendChild(link)
}

// view all profile info
function viewProfile(){
    viewBtn = document.getElementById('viewAll')
    viewBtn.onclick = function(event){
        scrollDiv = document.getElementById('scrollElem')
        event.preventDefault()
        var element1 = document.getElementById('userEmail')
        var element2 = document.getElementById('userLastLogin')
        var element3 = document.getElementById('userDateJoined')
        element1.style.display = 'block'
        element2.style.display = 'block'
        element3.style.display = 'block'
        scrollDiv.scrollIntoView({behavior: 'smooth'})
    }
}
function deletePrevent(){
    link = document.getElementById('editProfileBtn')
    about = document.getElementById('id_first_name')
    link.onclick = function(event){
        event.preventDefault()
        about.scrollIntoView({behavior: 'smooth'})
    }
}

// photos
function checkPhotos(){
    photosLink = document.getElementById('myPhotos')
    photosBlock = document.getElementById('photosBlock')

    photosLink.onclick = function(event){
        photosBlock.scrollIntoView({behavior: 'smooth'})
        photosBlock.style.boxShadow = '0 0 35px #303e47';
        setTimeout(function(){
            photosBlock.style.boxShadow = 'none'
        }, 1000)
        event.preventDefault()
    }
}

// friends
function getFriend(){
    var friendLink = document.getElementById('Friends');
    var friendBlock = document.getElementById('friendBlock');
    friendLink.onclick = function(event){
        event.preventDefault()
        if(friendBlock){
            friendBlock.scrollIntoView({behavior: 'smooth'})
            friendBlock.style.boxShadow = '0 0 35px #303e47';
            setTimeout(function(){
                friendBlock.style.boxShadow = 'none';
            }, 1000)
        }else{
            alert('У вас нет друзей')

        }
    }

}


document.addEventListener("DOMContentLoaded", function(){
status()
viewProfile()
deletePrevent()
getFriend()
checkPhotos()
});

