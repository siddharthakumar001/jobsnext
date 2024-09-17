const options = {
    debug: 'info',
    modules: {
        toolbar: '#toolbar-container'
    },
    theme: 'snow'
};
const editor = new Quill('#editor-container',options);

document.querySelector('#edit-btn').addEventListener('click', (e) => {
    document.querySelector('#bio').classList.add('d-none')
    document.querySelector('.quill-container').classList.remove('d-none')
})
// Edit user details
document.querySelector('#edit-bio').addEventListener('click' , (e) => {

    const data = []
    document.querySelector('.ql-editor').childNodes.forEach((node) => {
        data.push(node.outerHTML)
    })

    var formData = new FormData($("#edit-bio")[0]);
    formData.append('bio', data.join(''));

    $.ajax({
        type: "POST",
        url: "/edit_user",
        data: formData,
        async: false,
        cache: false,
        contentType: false,
        processData: false,
        success: function (res) {
          location.reload();
        
        }
});
} )
// end edit user details

// Delete user
document.getElementById('delete-account').onsubmit = (e) => {

    e.preventDefault()
    $.ajax({
        type: "DELETE",
        url: "/delete_user",
        dataType: 'json',
        success: function (res) {
          window.location.replace('/');
        
        }
});
       
}
// end delete user

document.querySelector('#contact-form').addEventListener('submit' , (e) => {
    e.preventDefault()
    const message = document.querySelector('#message')
    const button = document.querySelector('#submit-btn')
    button.innerHTML = 'sending...'
    button.disabled = true

    fetch ("/profile", {
        method: "POST",
        body: new FormData(e.target),
     })
        .then((response) => {
            button.disabled = false
            button.textContent = 'Send Message'

            if(!response.ok) {
                return response.text().then(text => { throw new Error(text) })
            } else {
                return response.json()
            }
        })
        .then((result) => {
            message.classList.remove('text-danger')
            message.classList.add('text-success')
            message.textContent = result.message
        })
        .catch((err) => {
            message.textContent = JSON.parse( err.toString().replace('Error: ','')).message
            message.classList.add('text-danger')
            message.classList.remove('text-success')
        })
})
