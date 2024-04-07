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

function getNavigationTiming() {
    let timingData = {};
    let navigationEntry = performance.getEntriesByType("navigation")[0];

    if (navigationEntry) {
        timingData.domInteractive = navigationEntry.domInteractive;
        timingData.domContentLoadedEventEnd = navigationEntry.domContentLoadedEventEnd;
        timingData.domComplete = navigationEntry.domComplete;
        timingData.loadEventEnd = navigationEntry.loadEventEnd;
    }

    return timingData;
}

function getDNSLookupTimes(hostname) {
    const resources = performance.getEntriesByType("resource");
    const resourceEntry = resources.find(entry => entry.name.includes(hostname));

    if (resourceEntry) {
        return resourceEntry.domainLookupEnd - resourceEntry.domainLookupStart;
    } else {
        return null;
    }
}

function getPerformanceMetrics() {
    const hostname = new URL(performance.getEntriesByType("navigation")[0].name).hostname;


    const metrics = {
        fcp: getContentfulPaints().fcp, 
        estimatedTBT: estimateBlockingTime(),
        navigationTiming: getNavigationTiming(),
        dnsLookupTimes: getDNSLookupTimes(hostname),
    };


    return metrics;
}