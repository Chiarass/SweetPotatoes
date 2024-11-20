#include <iostream>
#include <fstream>
#include <vector>
#include <string>
#include <cmath>
#include <TCanvas.h>
#include <TGraphErrors.h>
#include <TF1.h>
#include <TLegend.h>
#include <TLatex.h>
#include <TApplication.h>
#include <algorithm>

// Funzione per leggere dati da file
void readData(const std::string& filename, std::vector<double>& x, std::vector<double>& y, std::vector<double>& errx, std::vector<double>& erry) {
    std::ifstream file(filename);
    if (!file.is_open()) {
        std::cerr << "Errore: impossibile aprire il file " << filename << std::endl;
        return;
    }

    double xi, yi, exi, eyi;
    while (file >> xi >> yi >> exi >> eyi) {
        x.push_back(xi);
        y.push_back(yi);
        errx.push_back(exi);
        erry.push_back(eyi);
    }
    file.close();
}

// Funzione per eseguire i fit e visualizzare i grafici
void fitAndPlot() {
    // Lettura dei dati
    std::vector<double> x1, y1, errx1, erry1;
    std::vector<double> x2, y2, errx2, erry2;
    std::vector<double> x3, y3, errx3, erry3;

    readData("txt/test_1cal.txt", x1, y1, errx1, erry1);
    readData("txt/test_1expG.txt", x2, y2, errx2, erry2);
    readData("txt/test_1expS.txt", x3, y3, errx3, erry3);

    if (x1.empty() || x2.empty() || x3.empty()) {
        std::cerr << "Errore: uno o più file sono vuoti." << std::endl;
        return;
    }

    // Creazione dei TGraphErrors
    TGraphErrors* graph1 = new TGraphErrors(x1.size(), x1.data(), y1.data(), errx1.data(), erry1.data());
    TGraphErrors* graph2 = new TGraphErrors(x2.size(), x2.data(), y2.data(), errx2.data(), erry2.data());
    TGraphErrors* graph3 = new TGraphErrors(x3.size(), x3.data(), y3.data(), errx3.data(), erry3.data());

    // Range dinamico per i fit
    double x2_min = *std::min_element(x2.begin(), x2.end());
    double x2_max = *std::max_element(x2.begin(), x2.end());
    double x3_min = *std::min_element(x3.begin(), x3.end());
    double x3_max = *std::max_element(x3.begin(), x3.end());

    // Definizione delle funzioni di fit
    TF1* linearFunc = new TF1("linearFunc", "[0]*x + [1]", 0, 15);
    TF1* exponentialFuncG = new TF1("exponentialFuncG", "[0]*exp(x/[1])", x2_min, x2_max);
    TF1* exponentialFuncS = new TF1("exponentialFuncS", "[0]*exp(x/[1])", x3_min, x3_max);

    // Impostazione parametri iniziali
    exponentialFuncG->SetParameters(1, 0.1);
    exponentialFuncS->SetParameters(1, 0.1);

    // Esecuzione dei fit
    graph1->Fit(linearFunc, "Q");
    graph2->Fit(exponentialFuncG, "Q");
    graph3->Fit(exponentialFuncS, "Q");

    // Canvases per i grafici
    TCanvas* c1 = new TCanvas("c1", "Linear Fit", 800, 600);
    graph1->SetTitle("Retta di calibrazione;Multimetro;Oscilloscopio");
    graph1->SetMarkerStyle(21);
    graph1->Draw("AP");
    linearFunc->Draw("same");

    // Estrazione dei parametri e chi-squared
    double chi2_1 = linearFunc->GetChisquare();
    double ndf_1 = linearFunc->GetNDF();
    double reducedChi2_1 = chi2_1 / ndf_1;
    
    TLegend* legend1 = new TLegend(0.6, 0.7, 0.9, 0.9);
    legend1->AddEntry(graph1, "Dati", "lep");
    legend1->AddEntry(linearFunc, 
                      ("Fit Lineare: a=" + std::to_string(linearFunc->GetParameter(0)) + " ± " + 
                       std::to_string(linearFunc->GetParError(0)) + " b=" + std::to_string(linearFunc->GetParameter(1)) + 
                       " ± " + std::to_string(linearFunc->GetParError(1)) + 
                       "\nChi squared = " + std::to_string(chi2_1) + 
                       "\nChi squared ridotto = " + std::to_string(reducedChi2_1)).c_str(), 
                      "l");
    legend1->Draw();

    c1->Update();

    TCanvas* c2 = new TCanvas("c2", "Exponential Fit (Germanium)", 800, 600);
    graph2->SetTitle("Caratteristica I-V (Germanio);Tensione (V);Corrente (mA)");
    graph2->SetMarkerStyle(21);
    graph2->Draw("AP");
    exponentialFuncG->Draw("same");

    // Estrazione dei parametri e chi-squared
    double chi2_2 = exponentialFuncG->GetChisquare();
    double ndf_2 = exponentialFuncG->GetNDF();
    double reducedChi2_2 = chi2_2 / ndf_2;

    TLegend* legend2 = new TLegend(0.6, 0.7, 0.9, 0.9);
    legend2->AddEntry(graph2, "Dati", "lep");
    legend2->AddEntry(exponentialFuncG, 
                      ("Fit Esponenziale: c=" + std::to_string(exponentialFuncG->GetParameter(0)) + 
                       " ± " + std::to_string(exponentialFuncG->GetParError(0)) + " d=" + 
                       std::to_string(exponentialFuncG->GetParameter(1)) + 
                       " ± " + std::to_string(exponentialFuncG->GetParError(1)) + 
                       "\nChi squared = " + std::to_string(chi2_2) + 
                       "\nChi squared ridotto = " + std::to_string(reducedChi2_2)).c_str(), 
                      "l");
    legend2->Draw();

    c2->Update();

    TCanvas* c3 = new TCanvas("c3", "Exponential Fit (Silicium)", 800, 600);
    graph3->SetTitle("Caratteristica I-V (Silicio);Tensione (V);Corrente (mA)");
    graph3->SetMarkerStyle(21);
    graph3->Draw("AP");
    exponentialFuncS->Draw("same");

    // Estrazione dei parametri e chi-squared
    double chi2_3 = exponentialFuncS->GetChisquare();
    double ndf_3 = exponentialFuncS->GetNDF();
    double reducedChi2_3 = chi2_3 / ndf_3;

    TLegend* legend3 = new TLegend(0.6, 0.7, 0.9, 0.9);
    legend3->AddEntry(graph3, "Dati", "lep");
    legend3->AddEntry(exponentialFuncS, 
                      ("Fit Esponenziale: e=" + std::to_string(exponentialFuncS->GetParameter(0)) + 
                       " ± " + std::to_string(exponentialFuncS->GetParError(0)) + " f=" + 
                       std::to_string(exponentialFuncS->GetParameter(1)) + 
                       " ± " + std::to_string(exponentialFuncS->GetParError(1)) + 
                       "\nChi squared = " + std::to_string(chi2_3) + 
                       "\nChi squared ridotto = " + std::to_string(reducedChi2_3)).c_str(), 
                      "l");
    legend3->Draw();

    c3->Update();

    // Print results to the terminal
    std::cout << "=== Linear Fit ===" << std::endl;
    std::cout << "a = " << linearFunc->GetParameter(0) << " ± " << linearFunc->GetParError(0) << std::endl;
    std::cout << "b = " << linearFunc->GetParameter(1) << " ± " << linearFunc->GetParError(1) << std::endl;
    std::cout << "Chi squared: " << chi2_1 << std::endl;
    std::cout << "Reduced chi squared: " << reducedChi2_1 << std::endl;

    std::cout << "\n=== Exponential Fit (Germanium) ===" << std::endl;
    std::cout << "c = " << exponentialFuncG->GetParameter(0) << " ± " << exponentialFuncG->GetParError(0) << std::endl;
    std::cout << "d = " << exponentialFuncG->GetParameter(1) << " ± " << exponentialFuncG->GetParError(1) << std::endl;
    std::cout << "Chi squared: " << chi2_2 << std::endl;
    std::cout << "Reduced chi squared: " << reducedChi2_2 << std::endl;

    std::cout << "\n=== Exponential Fit (Silicium) ===" << std::endl;
    std::cout << "e = " << exponentialFuncS->GetParameter(0) << " ± " << exponentialFuncS->GetParError(0) << std::endl;
    std::cout << "f = " << exponentialFuncS->GetParameter(1) << " ± " << exponentialFuncS->GetParError(1) << std::endl;
    std::cout << "Chi squared: " << chi2_3 << std::endl;
    std::cout << "Reduced chi squared: " << reducedChi2_3 << std::endl;
}

int main(int argc, char** argv) {
    TApplication app("app", &argc, argv);
    fitAndPlot();
    app.Run();
    return 0;
}

