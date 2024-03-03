// This is the javascript file. The browser runs this file.
// I use it for sending data to the server
// When a form is submitted, it sends the data back and then
// shows the next thing.

console.log("Javascript file operational");

// Start Button
let button = document.getElementById("startButton")

// Divs
let hyperparameterFormDiv = document.getElementById("hyperparametersFormDiv");
let runOneGenomeDiv = document.getElementById("runOneGenomeDiv");
let fitnessFormDiv = document.getElementById("fitnessFormDiv");
let numberOfGenomesDiv = document.getElementById("numberOfGenomesDiv");
let finishedDiv = document.getElementById("finishedDiv");

// Forms
let hyperparameterForm = document.getElementById("hyperparametersForm");
let fitnessForm = document.getElementById("fitnessForm");

// Hyperparameter Form Elements
let mutationRateElement = document.getElementById("mutationRate");
let numberOfGenomesElement = document.getElementById("numberOfGenomes");
let percentageToDropElement = document.getElementById("percentageToDrop");
let iterationsAllowedElement = document.getElementById("iterationsAllowed");

// Fitness Form Elements
let x1Element = document.getElementById("x1");
let y1Element = document.getElementById("y1");
let x2Element = document.getElementById("x2");
let y2Element = document.getElementById("y2");
let identificationNumberElement = document.getElementById("identificationNumber");

// Verifys that a function doesn't chain requests
let hyperparametersAjaxRunning = false;
let runOneGenomeAjaxRunning = false;
let fitnessFormAjaxRunning = false;

// Hide Divs
hyperparameterFormDiv.style.display = "none";
runOneGenomeDiv.style.display = "none";
fitnessFormDiv.style.display = "none";
finishedDiv.style.display = "none";

// Function to download file
function downloadFile(data, name = "myData.txt") {
    const blob = new Blob([data], { type: "octet-stream" });

    const href = URL.createObjectURL(blob);

    const a = Object.assign(document.createElement("a"), {
        href,
        style: "display:none",
        download: name,
    });

    document.body.appendChild(a);

    a.click();
    URL.revokeObjectURL(href);
    a.remove();

}

// Handles Initial Start Button
function start(){
    hyperparameterFormDiv.style.display = "block";
    button.style.display = "none";
}

// Handles Hyperparameter Form
hyperparameterForm.addEventListener("submit", (e) => {
    e.preventDefault();

    if (hyperparametersAjaxRunning) return;
    hyperparametersAjaxRunning = true;

    let mutationRate = mutationRateElement.value;
    let numberOfGenomes = numberOfGenomesElement.value;
    let percentageToDrop = percentageToDropElement.value;
    let iterationsAllowed = iterationsAllowedElement.value;

    let postData = {
        "action": "sendHyperParameters",
        "mutationRate": mutationRate,
        "numberOfGenomes": numberOfGenomes,
        "percentageToDrop": percentageToDrop,
        "iterationsAllowed": iterationsAllowed
    }

    $.post("/api", postData, function( data ) {
        console.log(data)
        if (data == "Error") {
            alert("Uh oh! You screwed up :)");
            hyperparametersAjaxRunning = false
            return;
        }else{
        
            hyperparameterFormDiv.style.display = "none";
            runOneGenomeDiv.style.display = "block";
        }
    })

    hyperparametersAjaxRunning = false
})

// Handles runOneGenome
function runOneGenome(){

    if (runOneGenomeAjaxRunning) return;
    runOneGenomeAjaxRunning = true;

    let postData = {
        "action": "runOneGenome"
    }
    
    $.post("/api", postData, function( data ) {
        
        console.log(data)

        fitnessForm.style.display = "block"
        if (data == "Error") {
            alert("Error with runOneGenome");
            runOneGenomeAjaxRunning = false;
            return;
        }else{
            if (data.moreGenomes == "yes") {
                console.log("More Genomes")
                let genomeData = data.data; 
                let genomeIdentificationNumber = data.identificationNumber;

                downloadFile(genomeData, "genomeOutputData_" + genomeIdentificationNumber);
                alert("Remember this identification number: " + genomeIdentificationNumber);

                fitnessFormDiv.style.display = "block";
                runOneGenomeDiv.style.display = "none";
            }else if (data.moreGenomes == "no"){

                console.log("No More Genomes")
                let pickledGenerationData = data.pickledGenerationData
                let newGenomes = data.newGenomes

                downloadFile(pickledGenerationData, "pickledGenerationData")
                downloadFile(newGenomes, "newGenomes")
                alert("Congrats, you have finished a generation.")

            }
        }
    })

    runOneGenomeAjaxRunning = false;
}

// Handles Fitness Form
fitnessForm.addEventListener("submit", (e) => {
    e.preventDefault();

    if (fitnessFormAjaxRunning) return;
    fitnessFormAjaxRunning = true;

    let x1 = x1Element.value;
    let y1 = y1Element.value;
    let x2 = x2Element.value;
    let y2 = y2Element.value;

    let identificationNumber = identificationNumberElement.value;

    let postData = {
        "action": "sendFitnessData",
        "identificationNumber": identificationNumber,
        "x1": x1,
        "y1": y1,
        "x2": x2,
        "y2": y2
    }

    $.post("/api", postData, function( data ) {
        console.log(data)

        if (data === "Error") {
            alert("Error with fitness form")
            fitnessFormAjaxRunning = false;
            return;
        }else{
            fitnessFormDiv.style.display = "none";
            runOneGenomeDiv.style.display = "block";
        }
        
    })

    fitnessFormAjaxRunning = false;

})