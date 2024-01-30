import UIKit
import Charts

class DashboardViewController UIViewController {
     MARK - Properties
    lazy var lineChartView LineChartView = {
        let chartView = LineChartView()
        chartView.translatesAutoresizingMaskIntoConstraints = false
        return chartView
    }()
    
    lazy var noDataLabel UILabel = {
        let label = UILabel()
        label.text = Record Speed
        label.textAlignment = .center
        label.translatesAutoresizingMaskIntoConstraints = false
        label.isHidden = true
        return label
    }()

    var speedRecords [Double] = []  Array to store speed records
    var activityIndicator UIActivityIndicatorView!

     MARK - Lifecycle
    override func viewDidLoad() {
        super.viewDidLoad()
        setupUI()
        fetchLatestSpeedData()
    }

     MARK - UI Setup
    private func setupUI() {
        view.addSubview(lineChartView)
        view.addSubview(noDataLabel)
        setupChartViewConstraints()
        setupNoDataLabelConstraints()
        setupActivityIndicator()
    }
    
    private func setupChartViewConstraints() {
        NSLayoutConstraint.activate([
            lineChartView.topAnchor.constraint(equalTo view.safeAreaLayoutGuide.topAnchor),
            lineChartView.leadingAnchor.constraint(equalTo view.leadingAnchor),
            lineChartView.trailingAnchor.constraint(equalTo view.trailingAnchor),
            lineChartView.heightAnchor.constraint(equalTo view.heightAnchor, multiplier 0.5)
        ])
    }

    private func setupNoDataLabelConstraints() {
        NSLayoutConstraint.activate([
            noDataLabel.topAnchor.constraint(equalTo lineChartView.bottomAnchor),
            noDataLabel.leadingAnchor.constraint(equalTo view.leadingAnchor),
            noDataLabel.trailingAnchor.constraint(equalTo view.trailingAnchor),
            noDataLabel.bottomAnchor.constraint(equalTo view.safeAreaLayoutGuide.bottomAnchor)
        ])
    }
    
    private func setupActivityIndicator() {
        activityIndicator = UIActivityIndicatorView(style .medium)
        activityIndicator.center = view.center
        view.addSubview(activityIndicator)
    }

     MARK - Data Fetching
    private func fetchLatestSpeedData() {
        activityIndicator.startAnimating()
        NetworkService.fetchSpeedData { [weak self] result in
            DispatchQueue.main.async {
                self.activityIndicator.stopAnimating()
                switch result {
                case .success(let data)
                    self.speedRecords = data
                    self.updateChartData()
                case .failure
                    self.showErrorAlert()  Implement this method to show an error alert
                }
            }
        }
    }

     MARK - UI Update
    private func updateChartData() {
        if speedRecords.isEmpty {
            updateUIForNoData()
        } else {
            setChartData(speeds speedRecords)
            lineChartView.isHidden = false
            noDataLabel.isHidden = true
        }
    }

    private func setChartData(speeds [Double]) {
        let values = speeds.enumerated().map { ChartDataEntry(x Double($0.offset), y $0.element) }
        let set = LineChartDataSet(entries values, label Speed)

         Chart Customizations
        set.colors = [NSUIColor.blue]
        set.valueTextColor = NSUIColor.white
        set.circleRadius = 3
        set.circleColors = [NSUIColor.white]

        let data = LineChartData(dataSet set)
        lineChartView.data = data
         Additional chart customization (e.g., axis format, animation)
    }

    private func updateUIForNoData() {
        lineChartView.isHidden = true
        noDataLabel.isHidden = false
    }

    private func showErrorAlert() {
    let alert = UIAlertController(title: "Error", 
                                  message: "There was an error fetching speed data. Please try again later.", 
                                  preferredStyle: .alert)
    
    alert.addAction(UIAlertAction(title: "OK", style: .default))
    
    DispatchQueue.main.async {
        self.present(alert, animated: true, completion: nil)
    }
}

    }
}
