$('.add_cupcake').on('click', async function(e){
    e.preventDefault();
    await addCupcake();
    clearForm()
})

async function addCupcake(){
    const ccTable = $('.cupcakes')
    const flavor = $('#flavor').val()
    const rating = $('#rating').val()
    const size = $('#size').val()

    cc = {flavor: flavor,
        rating: rating,
        size: size
    }
   await axios.post('/api/cupcakes', cc)

    const newRow = `<tr><td>${flavor}</td><td>${rating}</td><td>${size}</td></tr>`

    ccTable.append(newRow)

}

function clearForm(){
    const flavor = $('#flavor').val('')
    const rating = $('#rating').val('')
    const size = $('#size').val('')
}


