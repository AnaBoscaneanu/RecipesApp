function confirmDelete(url, id) {
    result = confirm("Are you sure you want to delete this recipe?");
    if (result)
    {
        return fetch(url + '/' + id, {
            method: 'post',
            redirect: 'follow'
        })
        .then(function(response) {
            if (!response.ok) {
                console.log("Error", response);
            } else {
                console.log("Success", response);
                window.location.href = response.url
            }
        })
    }
}