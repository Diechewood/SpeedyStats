import Foundation

class SpeedCaptureViewModel {
    private let speedDataManager = SpeedDataManager()
    var speedData: [SpeedData] = []
    var isRecording: Bool = false

    // Callbacks for updates and errors
    var onSpeedDataUpdated: ((SpeedData) -> Void)?
    var onErrorOccurred: ((String) -> Void)?

    init() {
        setupSpeedDataManager()
    }

    private func setupSpeedDataManager() {
        speedDataManager.speedDataUpdated = { [weak self] speedData in
            self?.handleSpeedDataUpdate(speedData)
        }

        speedDataManager.errorOccurred = { [weak self] error in
            // Handle error, e.g., show an alert or log the error
            self?.onErrorOccurred?("Error in GPS tracking: \(error.localizedDescription)")
        }
    }

    func startRecording() {
        isRecording = true
        speedData.removeAll() // Clear previous data
        speedDataManager.startTracking()
    }

    func stopRecording() {
        isRecording = false
        speedDataManager.stopTracking()
        // Here the data would be saved or further processed
    }

    private func handleSpeedDataUpdate(_ newSpeedData: SpeedData) {
        guard isRecording else { return }
        speedData.append(newSpeedData)
        onSpeedDataUpdated?(newSpeedData)
    }

    // Additional functionalities can be added here

    // Example: Calculate average speed
    func calculateAverageSpeed() -> Double {
        guard !speedData.isEmpty else { return 0.0 }
        let totalSpeed = speedData.reduce(0) { $0 + $1.speed }
        return totalSpeed / Double(speedData.count)
    }

    // Example: Get top speed
    func getTopSpeed() -> Double {
        return speedData.max(by: { $0.speed < $1.speed })?.speed ?? 0.0
    }
}
