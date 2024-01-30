import Foundation

struct SpeedData {
    var speed: Double // Speed value in meters per second
    var timestamp: Date // Timestamp when the speed was recorded

    // Computed property to convert speed to miles per hour
    var speedInMilesPerHour: Double {
        return speed * 2.23694 // Conversion factor from meters/second to miles/hour
    }

    // Initializer for clarity and flexibility
    init(speed: Double, timestamp: Date = Date()) {
        self.speed = speed
        self.timestamp = timestamp
    }
}
