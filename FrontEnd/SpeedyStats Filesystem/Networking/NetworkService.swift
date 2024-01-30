import Foundation

class NetworkService {
    // Function to fetch speed data from a specified URL
    static func fetchSpeedData(completion: @escaping (Result<[Double], Error>) -> Void) {
        guard let url = URL(string: "https://your-api-endpoint.com/speedrecords") else { return }

        URLSession.shared.dataTask(with: url) { data, _, error in
            // Handle network errors
            if let error = error {
                completion(.failure(error))
                return
            }

            // Attempt to decode the received data
            guard let data = data, let fetchedData = try? JSONDecoder().decode([Double].self, from: data) else {
                completion(.failure(URLError(.badServerResponse)))
                return
            }

            // Return the fetched data
            completion(.success(fetchedData))
        }.resume()
    }
}
