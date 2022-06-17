
    window.onload=function(){
        let favoriteButtons = document.getElementsByClassName("favorite_button")
            for (var i =0; i< favoriteButtons.length; i++){
                favoriteButtons[i].addEventListener("click", function(){
                    fetch(`/favorite_programmers/${this.id}`,{method:"POST"})
                    .then(response => {
                    alert('favorited user')
                    })
                    .catch(error => {
                    // handle the error
                    console.log(error)
                    });
                })
            }
        }
       
    