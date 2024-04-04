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

function getTTI() {
    let fcp = performance.getEntriesByType('paint').filter(entry => entry.name === 'first-contentful-paint')[0].startTime;
    const longTaskThreshold = 50;

    let longResources = performance.getEntriesByType('resource').filter(entry => entry.duration > longTaskThreshold);

    let latestTaskEndTime = fcp;  
    longResources.forEach(task => {
        let endTime  = task.startTime + task.duration;
        latestTaskEndTime = Math.max(latestTaskEndTime, endTime); 
    });

    return latestTaskEndTime;
}

function getPerformanceMetrics() {
    
    const metrics = {
        fcp: getContentfulPaints().fcp, 
        estimatedTBT: estimateBlockingTime(),
        TTI: getTTI()
    };


    return metrics;
}