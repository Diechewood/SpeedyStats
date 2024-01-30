import UIKit
import CoreLocation

class TimerViewController: UIViewController {
    private var timer: Timer?
    private var elapsedTime: TimeInterval = 0
    private let speedDataManager = SpeedDataManager()
    private var isRecording = false

    // UI Components
    private let timerLabel: UILabel = {
        let label = UILabel()
        label.font = UIFont.monospacedDigitSystemFont(ofSize: 36, weight: .medium)
        label.textAlignment = .center
        label.text = "00:00:00"
        return label
    }()

    private let recordButton: UIButton = {
        let button = UIButton(type: .system)
        button.setTitle("Start Recording", for: .normal)
        button.backgroundColor = UIColor.red
        button.setTitleColor(.white, for: .normal)
        button.layer.cornerRadius = 25
        return button
    }()

    override func viewDidLoad() {
        super.viewDidLoad()
        setupUI()
        setupActions()
        setupSpeedDataManager()
    }

    private func setupUI() {
        view.backgroundColor = .white

        // Timer Label Layout
        timerLabel.translatesAutoresizingMaskIntoConstraints = false
        view.addSubview(timerLabel)

        NSLayoutConstraint.activate([
            timerLabel.centerXAnchor.constraint(equalTo: view.centerXAnchor),
            timerLabel.centerYAnchor.constraint(equalTo: view.centerYAnchor)
        ])

        // Record Button Layout
        recordButton.translatesAutoresizingMaskIntoConstraints = false
        view.addSubview(recordButton)

        NSLayoutConstraint.activate([
            recordButton.topAnchor.constraint(equalTo: timerLabel.bottomAnchor, constant: 20),
            recordButton.centerXAnchor.constraint(equalTo: view.centerXAnchor),
            recordButton.widthAnchor.constraint(equalToConstant: 200),
            recordButton.heightAnchor.constraint(equalToConstant: 50)
        ])
    }

    private func setupActions() {
        recordButton.addTarget(self, action: #selector(recordButtonTapped), for: .touchUpInside)
    }

    private func setupSpeedDataManager() {
        speedDataManager.speedDataUpdated = { [weak self] speedData in
            // Handle speed data update
            // Update the UI if necessary, but ensure this is done on the main thread
        }

        speedDataManager.errorOccurred = { [weak self] error in
            // Handle errors from SpeedDataManager
            DispatchQueue.main.async {
                self?.showErrorAlert(message: error.localizedDescription)
            }
        }
    }

    @objc private func recordButtonTapped() {
        isRecording.toggle()
        if isRecording {
            startRecording()
            recordButton.setTitle("Stop Recording", for: .normal)
        } else {
            stopRecording()
            recordButton.setTitle("Start Recording", for: .normal)
        }
    }

    private func startRecording() {
        speedDataManager.startTracking()
        timer = Timer.scheduledTimer(withTimeInterval: 1.0, repeats: true) { [weak self] _ in
            self?.updateTimer()
        }
    }

    private func stopRecording() {
        speedDataManager.stopTracking()
        timer?.invalidate()
        timer = nil
        elapsedTime = 0
        timerLabel.text = "00:00:00"

        // Save recording data to the database here
        // Consider performing this operation in a background thread
    }

    private func updateTimer() {
        elapsedTime += 1
        timerLabel.text = formatTimeInterval(elapsedTime)
    }

    private func formatTimeInterval(_ interval: TimeInterval) -> String {
        let hours = Int(interval) / 3600
        let minutes = Int(interval) / 60 % 60
        let seconds = Int(interval) % 60
        return String(format: "%02i:%02i:%02i", hours, minutes, seconds)
    }

    private func showErrorAlert(message: String) {
        let alert = UIAlertController(title: "Error", message: message, preferredStyle: .alert)
        alert.addAction(UIAlertAction(title: "OK", style: .default, handler: nil))
        present(alert, animated: true)
    }
}
