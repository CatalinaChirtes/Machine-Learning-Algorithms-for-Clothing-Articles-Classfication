import { HttpClient } from "@angular/common/http";
import { Injectable } from "@angular/core";
import { environment } from "../../environments/environment";
import { Observable } from "rxjs";
import { AccuracyPerCategoryModel } from "../_models/AccuracyPerCategoryModel";
import { AccuracyPerArticleTypeModel } from "../_models/AccuracyPerArticleTypeModel";

@Injectable({
    providedIn: 'root'
})
export class AccuracyService {
    constructor(protected http: HttpClient){}

    private baseCnnAccuracyPerCategoryPath = environment.apiUrlCnnAccuracyPerCategory;
    private baseCnnAccuracyPerArticleTypePath = environment.apiUrlCnnAccuracyPerArticleType;

    private baseMobileNetV2AccuracyPerCategoryPath = environment.apiUrlMobileNetV2AccuracyPerCategory;
    private baseMobileNetV2AccuracyPerArticleTypePath = environment.apiUrlMobileNetV2AccuracyPerArticleType;

    private baseInceptionResNetV2AccuracyPerCategoryPath = environment.apiUrlInceptionResNetV2AccuracyPerCategory;
    private baseInceptionResNetV2AccuracyPerArticleTypePath = environment.apiUrlInceptionResNetV2AccuracyPerArticleType;

    // CNN Models
    public ApiCnnAccuracyPerCategoryGet(): Observable<AccuracyPerCategoryModel>{
        return this.http.get<AccuracyPerCategoryModel>(this.baseCnnAccuracyPerCategoryPath)
    }

    public ApiCnnAccuracyPerArticleTypeGet(): Observable<AccuracyPerArticleTypeModel>{
        return this.http.get<AccuracyPerArticleTypeModel>(this.baseCnnAccuracyPerArticleTypePath)
    }

    // MobileNetV2 Models
    public ApiMobileNetV2AccuracyPerCategoryGet(): Observable<AccuracyPerCategoryModel>{
        return this.http.get<AccuracyPerCategoryModel>(this.baseMobileNetV2AccuracyPerCategoryPath)
    }

    public ApiMobileNetV2AccuracyPerArticleTypeGet(): Observable<AccuracyPerArticleTypeModel>{
        return this.http.get<AccuracyPerArticleTypeModel>(this.baseMobileNetV2AccuracyPerArticleTypePath)
    }

    // InceptionResNetV2 Models
    public ApiInceptionResNetV2AccuracyPerCategoryGet(): Observable<AccuracyPerCategoryModel>{
        return this.http.get<AccuracyPerCategoryModel>(this.baseInceptionResNetV2AccuracyPerCategoryPath)
    }

    public ApiInceptionResNetV2AccuracyPerArticleTypeGet(): Observable<AccuracyPerArticleTypeModel>{
        return this.http.get<AccuracyPerArticleTypeModel>(this.baseInceptionResNetV2AccuracyPerArticleTypePath)
    }
}