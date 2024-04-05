function getContentfulPaints() {
    const paintTimings = performance.getEntriesByType("paint");
    const fcpEntry = paintTimings.find(entry => entry.name === "first-contentful-paint");
  
    return {
      fcp: fcpEntry ? fcpEntry.startTime : null,
    };
}
  

  //return getContentfulPaints(); 

function estimateBlockingTime() {
    console.log("estimateBlockingTime function executing...");

    const performanceEntries = performance.getEntriesByType("navigation");

    if (performanceEntries.length === 0) {
        console.log("No navigation entries found");
        return;
    }

    const navigationEntry = performanceEntries[0];

    const startTime = navigationEntry.startTime;
    const loadEventEnd = navigationEntry.loadEventEnd;
    const estimatedTBT = (loadEventEnd - startTime) * 0.6;

    console.log("Estimated Total Blocking Time: ", estimatedTBT);

    return estimatedTBT;
}

//const estimatedTBT = estimateBlockingTime();

/*
function getApproxTTI() {
    let fcp = performance.getEntriesByType('paint').filter(entry => entry.name === 'first-contentful-paint')[0].startTime;
    const longTaskThreshold = 1;

    let longResources = performance.getEntriesByType('resource').filter(entry => entry.duration > longTaskThreshold);

    let latestTaskEndTime = fcp;  
    longResources.forEach(task => {
        let endTime  = task.startTime + task.duration;
        console.log("Task Start:", task.startTime, "End:", endTime);
        latestTaskEndTime = Math.max(latestTaskEndTime, endTime); 
    });

    console.log("Final latestTaskEndTime:", latestTaskEndTime);
    return latestTaskEndTime;
}
*/

function getApproxTTI() {
    let fcp = performance.getEntriesByType('paint').filter(entry => entry.name === 'first-contentful-paint')[0].startTime;
    const scriptThreshold = 10;

    let potentialTTIEndMarkers = [fcp];

    let longResources = performance.getEntriesByType('resource').filter(entry => entry.duration > scriptThreshold);

    longResources.forEach(task => potentialTTIEndMarkers.push(task.startTime + task.duration));

    performance.getEntriesByType('script').forEach(scriptEntry => {
        potentialTTIEndMarkers.push(scriptEntry.startTime + scriptEntry.duration);

    });
    
    let domLoaded = performance.getEntriesByType('navigation').filter(entry => entry.type === 'domContentLoaded')[0].domContentLoadedEventEnd;
    potentialTTIEndMarkers.push(domLoaded);


    let latestActivityEnd = Math.max(...potentialTTIEndMarkers);
    return latestActivityEnd
}


function getPerformanceMetrics() {
    
    const metrics = {
        fcp: getContentfulPaints().fcp, 
        estimatedTBT: estimateBlockingTime(),
        TTI: getApproxTTI()
    };


    return metrics;
}