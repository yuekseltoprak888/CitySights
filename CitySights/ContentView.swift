//
//  ContentView.swift
//  CitySights
//
//  Created by Yüksel Toprak on 14.02.25.
//

import SwiftUI

struct ContentView: View {
    @State var query: String = ""

    private var buttonGo: some View {
        Button {

        } label: {
            Text("Go")
        }
        .buttonStyle(.borderedProminent)

    }
    var body: some View {
        VStack {
            HStack(alignment: .center) {
                TextField("Search", text: $query)
                    .textFieldStyle(.roundedBorder)
                    .font(.title)
                    .multilineTextAlignment(.center)
                buttonGo
                    .onAppear {
                        print(Bundle.main.infoDictionary!["API_KEY"] as? String)
                    }

            }




        }
        .padding()
    }
}

#Preview {
    ContentView()
}
