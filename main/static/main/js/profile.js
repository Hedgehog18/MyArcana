let cropper;
const avatarButton = document.getElementById('avatarButton');
const inputAvatar = document.getElementById('inputAvatar');
const avatarPreview = document.getElementById('avatarPreview');
const avatarForm = document.getElementById('avatarForm');

inputAvatar.addEventListener('change', function(e) {
    const file = e.target.files[0];
    if (!file) return;

    const reader = new FileReader();
    reader.onload = function(event) {
        avatarPreview.src = event.target.result;
        if (cropper) cropper.destroy();
        cropper = new Cropper(avatarPreview, {
            aspectRatio: 1,
            viewMode: 1,
            autoCropArea: 1
        });

        avatarButton.innerHTML = "Зберегти аватар";
    };
    reader.readAsDataURL(file);
});

avatarButton.addEventListener('click', function() {
    if (cropper) {
        cropper.getCroppedCanvas({ width: 300, height: 300 })
            .toBlob(function(blob) {
                const reader = new FileReader();
                reader.onloadend = function() {
                    document.getElementById('croppedAvatarData').value = reader.result;
                    avatarForm.submit();
                }
                reader.readAsDataURL(blob);
            }, 'image/png');
    }
});

function showBirthDateInput() {
    document.getElementById('birthDateInputContainer').style.display = 'block';
}