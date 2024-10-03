function getContentfulPaints() {
    // Get first contentful paint
    const paintTimings = performance.getEntriesByType("paint");
    console.log("paintTimings: ", paintTimings);
    const fcpEntry = paintTimings.find(entry => entry.name === "first-contentful-paint");
  
    return {
      fcp: fcpEntry ? fcpEntry.startTime : null,
    };
}
  


// Tried to implement own function to estimate blocking time.
// Left in at time of collection, but not used in final analysis.
function estimateBlockingTime(navigationEntry) {
    console.log("estimateBlockingTime function executing...");

    

    if (navigationEntry.length === 0) {
        console.log("No navigation entries found");
        return;
    }

    const navigationEntry_zero = navigationEntry[0];

    const startTime = navigationEntry_zero.startTime;
    const loadEventEnd = navigationEntry_zero.loadEventEnd;
    const estimatedTBT = (loadEventEnd - startTime) * 0.6;

    console.log("Estimated Total Blocking Time: ", estimatedTBT);

    return estimatedTBT;
}


// Function to get navigation timing data
function getNavigationTiming(navigationEntry) {
    let timingData = {};
    const navigationEntry_zero = navigationEntry[0];

    if (navigationEntry_zero) {
        timingData.navigationStart = navigationEntry_zero.navigationStart;
        timingData.fetchStart = navigationEntry_zero.fetchStart;
        timingData.domainLookupStart = navigationEntry_zero.domainLookupStart;
        timingData.domainLookupEnd = navigationEntry_zero.domainLookupEnd;
        timingData.connectStart = navigationEntry_zero.connectStart;
        timingData.connectEnd = navigationEntry_zero.connectEnd;
        timingData.secureConnectionStart = navigationEntry_zero.secureConnectionStart;
        timingData.domInteractive = navigationEntry_zero.domInteractive;
        timingData.domContentLoadedEventStart = navigationEntry_zero.domContentLoadedEventStart;
        timingData.domContentLoadedEventEnd = navigationEntry_zero.domContentLoadedEventEnd;
        timingData.domComplete = navigationEntry_zero.domComplete;
        timingData.domloading = navigationEntry_zero.domLoading;
        timingData.domInteractive = navigationEntry_zero.domInteractive;
        timingData.loadEventStart = navigationEntry_zero.loadEventStart;
        timingData.loadEventEnd = navigationEntry_zero.loadEventEnd;
        timingData.requestStart = navigationEntry_zero.requestStart;
        timingData.responseStart = navigationEntry_zero.responseStart;
        timingData.responseEnd = navigationEntry_zero.responseEnd;
        timingData.loadEventStart = navigationEntry_zero.loadEventStart;
        timingData.loadEventEnd = navigationEntry_zero.loadEventEnd;

    }

    return timingData;
}

// Function to get DNS lookup times. When starting analysis, turned out to be unusable.
function getDNSLookupTimes(hostname) {
    const resources = performance.getEntriesByType("resource");
    const resourceEntry = resources.find(entry => entry.name.includes(hostname));

    if (resourceEntry) {
        return resourceEntry.domainLookupEnd - resourceEntry.domainLookupStart;
    } else {
        return null;
    }
}

// Turned out to be unusable bc tor browser clamps it to 100ms
function recordNavigationStartTime() {
    window.pythonPageLoadStartTime = performance.now();
}


// Gather all metrics from the different functions to pass them back to the pythhon script
function getPerformanceMetrics(navigationEntry) {
    const hostname = new URL(navigationEntry[0].name).hostname;

    const metrics = {
        fcp: getContentfulPaints(navigationEntry).fcp, 
        estimatedTBT: estimateBlockingTime(navigationEntry),
        navigationTiming: getNavigationTiming(navigationEntry),
        dnsLookupTimes: getDNSLookupTimes(hostname),

    };


    return metrics;
}

recordNavigationStartTime();
const navigationEntry = performance.getEntriesByType("navigation");
console.log("pythonPageLoadStartTime: ", window.pythonPageLoadStartTime);