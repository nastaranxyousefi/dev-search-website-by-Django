let searchForm = document.getElementById('searchForm')  //accessing to searchForm
    let pageLinks = document.getElementsByClassName('page-link') //accessing to page links

    //Ensure search for exists
    if(searchForm){
        for(let i=0; pageLinks.length > i; i++){
            pageLinks[i].addEventListener('click', function (e) {
                e.preventDefault()

                //get the Data attribute
                let page = this.dataset.page

                //Add hidden search input to form
                searchForm.innerHTML += `<input value=${page} name="page" hidden/>`

                //submit form
                searchForm.submit()
            })
        }
    }
