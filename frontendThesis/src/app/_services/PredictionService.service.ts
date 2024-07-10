import { HttpClient } from "@angular/common/http";
import { Injectable } from "@angular/core";
import { environment } from "../../environments/environment";
import { Observable } from "rxjs";
import { PredictionModel } from "../_models/PredictionModel";

@Injectable({
    providedIn: 'root'
})
export class PredictionService {
    constructor(protected http: HttpClient){}

    private baseCnnPredictionModelPath = environment.apiUrlCnnPredictionModel;
    private baseMobileNetV2PredictionModelPath = environment.apiUrlMobileNetV2PredictionModel;
    private baseInceptionResNetV2PredictionModelPath = environment.apiUrlInceptionResNetV2PredictionModel;


    public ApiCnnPredictionPost(file: File): Observable<PredictionModel>{
        const formData = new FormData();
        formData.append('file', file);

        return this.http.post<PredictionModel>(
            `${this.baseCnnPredictionModelPath}`,
            formData
        )
    }

    public ApiMobileNetV2PredictionPost(file: File): Observable<PredictionModel>{
        const formData = new FormData();
        formData.append('file', file);

        return this.http.post<PredictionModel>(
            `${this.baseMobileNetV2PredictionModelPath}`,
            formData
        )
    }

    public ApiInceptionResNetV2PredictionPost(file: File): Observable<PredictionModel>{
        const formData = new FormData();
        formData.append('file', file);

        return this.http.post<PredictionModel>(
            `${this.baseInceptionResNetV2PredictionModelPath}`,
            formData
        )
    }
}