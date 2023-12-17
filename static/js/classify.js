const fetchedData = fetch('http://127.0.0.1:8989/record', {
    headers: {
        'Content-Type': "application/json",
    },
})
fecthedData
    .then(response => response.json())
    .then((data) => {
        console.log(data)
        document.getElementById("sentiment").innerText = JSON.stringify(data)
    })

