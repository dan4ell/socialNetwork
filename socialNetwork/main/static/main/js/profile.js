profileBtn = document.getElementById('profile-btn');
profileUl = document.getElementById('profile-ul');
profileBtn.addEventListener('click', function(){
var computedStyle = window.getComputedStyle(profileUl);
var displayValue = computedStyle.getPropertyValue('display');
if (displayValue === 'none'){
    profileUl.style.display = 'block';
}
else{
    profileUl.style.display = 'none';
}
})