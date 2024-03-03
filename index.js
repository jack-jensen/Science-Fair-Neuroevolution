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
    hyperparameterFormDiv.style.display = "block";
    button.style.display = "none";
}

// // Handles Pickle Form
// pickleForm.addEventListener("submit", (e) => {
//     e.preventDefault();

//     if (pickleFormAjaxRunning) return;
//     pickleFormAjaxRunning = true;

//     let formData = new FormData(pickleForm); // Create FormData object from the form
    
//     console.log(formData.value)

//     $.ajax({
//         url: "/api",
//         type: "POST",
//         data: formData, // Use FormData object directly
//         contentType: false, // Set contentType to false to prevent jQuery from setting it automatically
//         processData: false, // Set processData to false to prevent jQuery from processing the data
//         success: function(data) {
//             console.log(data);
//             hyperparameterFormDiv.style.display = "block";
//             pickleFormDiv.style.display = "none";

//             if (firstTime != "y") {
//                 numberOfGenomesDiv.style.display = "none";
//             }
//         },
//         error: function(xhr, status, error) {
//             console.error(error);
//             alert("Error with ajax")
//         },
//         complete: function() {
//             pickleFormAjaxRunning = false;
//         }
//     });
// });

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
    console.log("1")

    if (runOneGenomeAjaxRunning) return;
    runOneGenomeAjaxRunning = true;
    
    console.log("2")

    let postData = {
        "action": "runOneGenome"
    }
    
    console.log("3")

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
                // finishedDiv.style.display = "block";
                // runOneGenomeDiv.style.display = "none";
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



