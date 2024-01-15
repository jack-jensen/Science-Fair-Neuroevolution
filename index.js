gatherDataAjaxRunning = false;

let form = document.getElementById("form");
let green = document.getElementById("green");
let fitnessScorer = document.getElementById("fitnessScorer")

green.style.display = "none";
form.style.display = "none";
fitnessScorer.style.display = "none";

form.addEventListener("submit", (e) => {
    e.preventDefault();



    if (gatherDataAjaxRunning) return;
    gatherDataAjaxRunning = true;

    let file = document.getElementById("genomeFile")

    let postData = {
        "action": "sendPickledGenomes",
        "file": file
    }

    $.post("/api", postData, function( data ) {

        if (data.status == "Wrong number of genomes") {
            alert("The file did not have the correct number of genomes.");
            return;
        }else{
            green.style.display = "block";
            gatherDataAjaxRunning = false;
        }



    })

})

let fitnessScorerAjaxRunning = false

fitnessScorer.addEventListener("submit", (e) => {
    e.preventDefault();

    if (fitnessScorerAjaxRunning) return;

    fitnessScorerAjaxRunning = true

    let distance = document.getElementById("distance")
    let postData = {
        "action": "sendFitnessData",
        "distance": distance.value
    }

    $.post("/api", postData, function( data ) {
        let 
    })

})

function start(){
    form.style.display = "block"
    form.style.borderStyle = "solid"
    let button = document.getElementById("startButton")

    button.style.display = "none"
}

let greenLightAjaxRunning = false

function greenLight(){

    if (greenLightAjaxRunning) return;

    greenLightAjaxRunning = true;

    let postData = {
        "action": "greenLight"
    }

    $.post("/api", postData, function( data ) {

        fitnessScorer.style.display = "block"
    })
}