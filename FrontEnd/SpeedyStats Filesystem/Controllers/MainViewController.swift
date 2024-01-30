import UIKit

class MainViewController: UITabBarController {

    override func viewDidLoad() {
        super.viewDidLoad()

        // Setting up the individual view controllers for each tab
        let dashboardVC = DashboardViewController()
        dashboardVC.tabBarItem = UITabBarItem(title: "Dashboard", image: UIImage(systemName: "speedometer"), tag: 0)

        let timerVC = TimerViewController()
        timerVC.tabBarItem = UITabBarItem(title: "Timer", image: UIImage(systemName: "timer"), tag: 1)

        let accountVC = AccountViewController()
        accountVC.tabBarItem = UITabBarItem(title: "Account", image: UIImage(systemName: "person.crop.circle"), tag: 2)

        // Embedding each ViewController in a UINavigationController
        let controllers = [dashboardVC, timerVC, accountVC].map { UINavigationController(rootViewController: $0) }
        viewControllers = controllers

        // Additional Tab Bar Customizations (if required)
        customizeTabBarAppearance()
    }

    private func customizeTabBarAppearance() {
        // Customize the appearance of the tab bar here
        // For example, setting the tab bar's background color or item tint color
        tabBar.tintColor = .systemBlue // Color for the selected item
        tabBar.barTintColor = .white // Background color of the tab bar
        tabBar.unselectedItemTintColor = .gray // Color for unselected items
    }

    // Additional functions and configurations can be added here as needed
}
