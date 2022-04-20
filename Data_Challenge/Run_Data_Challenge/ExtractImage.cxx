void ExtractImage();

void ExtractImage() {

	//Read in the source file, extract the Canvas, and save the histogram
	TFile * f1 = new TFile("sim_image.root");
	//To get canvas name for below run: f1->ls() 
	TCanvas * C = (TCanvas*)f1->Get("Image___iteration__20___22");
	//To get hist name for below run: C->GetListOfPrimitives()->Print()
	TH2D * hist1 = (TH2D*)C->GetPrimitive("Image___iteration__20___22Hist");

	//Re draw the histogram
	TCanvas * C1 = new TCanvas();
	hist1->Draw();
		
	//write to file:
	ofstream myfile;
	myfile.open ("extracted_image.dat");
	myfile<<"Binx	Biny	Phi_LowerEdge[deg]	Phi_HigherEdge[deg]	Phi_center[deg]	Theta_LowerEdge[deg]	Theta_HigherEdge[deg]	Theta_center[deg]	Intensity[a.u.]"<<endl;

	//Print the counts for each bin
	for (int i = 1; i <= hist1->GetXaxis()->GetNbins(); i++) {
		for (int j = 1; j <= hist1->GetYaxis()->GetNbins(); j++){
		
		//write to file:
		myfile<<i<<"\t"<<j<<"\t"<<hist1->GetXaxis()->GetBinLowEdge(i)<<"\t"<<hist1->GetXaxis()->GetBinUpEdge(i)<<"\t"<<hist1->GetXaxis()->GetBinCenter(i)<<"\t"<<hist1->GetYaxis()->GetBinLowEdge(j)<<"\t"<<hist1->GetYaxis()->GetBinUpEdge(j)<<"\t"<<hist1->GetYaxis()->GetBinCenter(j)<<"\t"<<hist1->GetBinContent(i,j)<<endl;
		
		}
	
	}

}

