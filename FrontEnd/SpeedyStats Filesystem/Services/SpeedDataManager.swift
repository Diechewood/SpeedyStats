import Foundation
import CoreLocation

class SpeedDataManager: NSObject, CLLocationManagerDelegate {
    private let locationManager = CLLocationManager()
    var speedDataUpdated: ((SpeedData) -> Void)?
    var errorOccurred: ((Error) -> Void)?

    override init() {
        super.init()
        setupLocationManager()
    }

    private func setupLocationManager() {
        locationManager.delegate = self
        locationManager.desiredAccuracy = kCLLocationAccuracyBestForNavigation
        locationManager.activityType = .fitness // Adjust based on app's use case
        locationManager.requestWhenInUseAuthorization()
    }

    func startTracking() {
        guard CLLocationManager.locationServicesEnabled() else {
            errorOccurred?(NSError(domain: "LocationServices", code: -1, userInfo: [NSLocalizedDescriptionKey: "Location services are disabled."]))
            return
        }
        locationManager.startUpdatingLocation()
    }

    func stopTracking() {
        locationManager.stopUpdatingLocation()
    }

    // CLLocationManagerDelegate methods
    func locationManager(_ manager: CLLocationManager, didUpdateLocations locations: [CLLocation]) {
        guard let currentLocation = locations.last, currentLocation.speed >= 0 else { return }
        
        let speedData = SpeedData(speed: currentLocation.speed, timestamp: currentLocation.timestamp)
        speedDataUpdated?(speedData)
    }

    func locationManager(_ manager: CLLocationManager, didFailWithError error: Error) {
        errorOccurred?(error)
    }

    func locationManager(_ manager: CLLocationManager, didChangeAuthorization status: CLAuthorizationStatus) {
        if status == .restricted || status == .denied {
            // Inform the user or the app that location services are restricted/denied
            errorOccurred?(NSError(domain: "LocationAuthorization", code: -1, userInfo: [NSLocalizedDescriptionKey: "Location authorization denied."]))
        }
    }
}
