console.log("Javascript file operational");

// Start Button
let button = document.getElementById("startButton")

// Divs
let pickleFormDiv = document.getElementById("pickleFormDiv");
let hyperparameterFormDiv = document.getElementById("hyperparametersFormDiv");
let runOneGenomeDiv = document.getElementById("runOneGenomeDiv");
let fitnessFormDiv = document.getElementById("fitnessFormDiv");
let numberOfGenomesDiv = document.getElementById("numberOfGenomesDiv");

// Forms
let pickleForm = document.getElementById("pickleForm");
let hyperparameterForm = document.getElementById("hyperparametersForm");
let fitnessForm = document.getElementById("fitnessForm");

// Pickle Form Elements
let fileElement = document.getElementById("genomeFile");
let firstTimeElement = document.getElementById("firstTime");
let numberOfGenomesExpectedElement = document.getElementById("numberOfGenomesExpected");

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
let pickleFormAjaxRunning = false;
let hyperparametersAjaxRunning = false;
let runOneGenomeAjaxRunning = false;
let fitnessFormAjaxRunning = false;

// Hide Divs
pickleFormDiv.style.display = "none";
hyperparameterFormDiv.style.display = "none";
runOneGenomeDiv.style.display = "none";
fitnessFormDiv.style.display = "none";

// Function to download file. Credit to video link:
// https://www.youtube.com/watch?v=io2blfAlO6E
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
    pickleFormDiv.style.display = "block";
    pickleFormDiv.style.borderStyle = "solid";
    button.style.display = "none";
}

// Handles Pickle Form
pickleForm.addEventListener("submit", (e) => {
    e.preventDefault();

    if (pickleFormAjaxRunning) return;
    pickleFormAjaxRunning = true;

    let file = fileElement.files[0];
    let firstTime = firstTimeElement.value;
    let numberOfGenomesExpected = numberOfGenomesExpectedElement.value;

    if (file == null) {
        file = "none";
    }

    let postData = {
        "action": "sendPickledGenomes",
        "file": file,
        "firstTime": firstTime,
        "numberOfGenomesExpected": numberOfGenomesExpected

    }

    $.post("/api", postData, function( data ) {

        console.log(data)

        if (data == "Error") {

            alert("Error with Pickling");
            pickleFormAjaxRunning = false;
            return;
        }else{

            hyperparameterFormDiv.style.display = "block";
            pickleFormDiv.style.display = "none";

            if (firstTime != "y") {
                numberOfGenomesDiv.style.display = "none";
            }
        }
    })

    pickleFormAjaxRunning = false;
})

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

        fitnessForm.style.display = "block"
        if (data == "Error") {
            alert("Error with runOneGenome");
            runOneGenomeAjaxRunning = false;
            return;
        }else{
            let genomeData = data.data;
            let genomeIdentificationNumber = data.identificationNumber;

            downloadFile(genomeData, "genomeOutputData_" + genomeIdentificationNumber);
            alert("Remember this identification number: " + genomeIdentificationNumber);


            fitnessFormDiv.style.display = "block";
            runOneGenomeDiv.style.display = "none";
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
