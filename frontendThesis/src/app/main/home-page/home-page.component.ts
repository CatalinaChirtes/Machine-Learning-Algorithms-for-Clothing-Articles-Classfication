import { AfterViewInit, ChangeDetectorRef, Component, OnInit, ViewChild } from '@angular/core';
import { PredictionService } from '../../_services/PredictionService.service';
import { PredictionModel } from '../../_models/PredictionModel';
import { AccuracyPerCategoryModel } from '../../_models/AccuracyPerCategoryModel';
import { AccuracyService } from '../../_services/AccuracyService.service';
import {
  ApexChart,
  ApexAxisChartSeries,
  ChartComponent,
  ApexDataLabels,
  ApexPlotOptions,
  ApexYAxis,
  ApexLegend,
  ApexGrid
} from "ng-apexcharts";
import { AccuracyPerArticleTypeModel } from '../../_models/AccuracyPerArticleTypeModel';
import { Observable, forkJoin } from 'rxjs';
import { Route, Router } from '@angular/router';

type ApexXAxis = {
  type?: "category" | "datetime" | "numeric";
  categories?: any;
  labels?: {
    style?: {
      colors?: string | string[];
      fontSize?: string;
    };
  };
};

export type ChartOptions = {
  series: ApexAxisChartSeries;
  chart: ApexChart;
  dataLabels: ApexDataLabels;
  plotOptions: ApexPlotOptions;
  yaxis: ApexYAxis;
  xaxis: ApexXAxis;
  grid: ApexGrid;
  colors: string[];
  legend: ApexLegend;
};

@Component({
  selector: 'app-home-page',
  templateUrl: './home-page.component.html',
  styleUrl: './home-page.component.scss'
})
export class HomePageComponent implements OnInit, AfterViewInit {
  @ViewChild("chart") chart!: ChartComponent | undefined;
  public chartCategoryOptions: Partial<ChartOptions> | any;
  public chartArticleTypeOptions: Partial<ChartOptions> | any;
  public accuracyPerCategoryModel: AccuracyPerCategoryModel | null = null;
  public accuracyPerArticleTypeModel: AccuracyPerArticleTypeModel | null = null;

  constructor(
  private accuracyService: AccuracyService,
  private cdr: ChangeDetectorRef,
  private router: Router ) 
  { 
    this.chartCategoryOptions = {
      series: [],
      chart: {
        type: "bar",
        height: 350,
        events: { }
      },
      colors: [
        "#4a148c5b", 
        "#7fd3e8",
        "#eccf4f"
      ],
      plotOptions: {
        bar: {
          columnWidth: "60%",
          distributed: false
        }
      },
      dataLabels: {
        enabled: false
      },
      legend: {
        show: true,
        position: 'bottom'
      },
      grid: {
        show: false
      },
      xaxis: {
        categories: [
          "Bags",
          "Bottomwear",
          "Dress",
          "Shoes",
          "Topwear"
        ],
        labels: {
          style: {
            colors: [],
            fontSize: "12px"
          }
        }
      }
    };

    this.chartArticleTypeOptions = {
      series: [],
      chart: {
        type: "bar",
        height: 350,
        events: { }
      },
      colors: [
        "#4a148c5b", 
        "#7fd3e8",
        "#eccf4f"
      ],
      plotOptions: {
        bar: {
          columnWidth: "60%",
          distributed: false
        }
      },
      dataLabels: {
        enabled: false
      },
      legend: {
        show: true,
        position: 'bottom'
      },
      grid: {
        show: false
      },
      xaxis: {
        categories: [
          "Backpacks", 
          "Capris", 
          "Casual Shoes", 
          "Clutches", 
          "Dresses", 
          "Flats", 
          "Flip Flops", 
          "Formal Shoes", 
          "Handbags", 
          "Heels", 
          "Jackets", 
          "Jeans", 
          "Laptop Bag", 
          "Leggings", 
          "Sandals", 
          "Shirts", 
          "Shorts", 
          "Skirts", 
          "Sports Shoes", 
          "Sweaters", 
          "Tops", 
          "Track Pants", 
          "Trousers", 
          "Tshirts"
        ],
        labels: {
          style: {
            colors: [],
            fontSize: "12px"
          }
        }
      }
    };
  }

  ngOnInit(): void {
    this.fetchAccuracyPerCategoryData();
    this.fetchAccuracyPerArticleTypeData();
  }

  ngAfterViewInit(): void {
    setTimeout(() => {
      this.redrawCharts();
    }, 100);
  }
  
  fetchAccuracyPerCategoryData() {
    const cnnAccuracy$: Observable<AccuracyPerCategoryModel> = this.accuracyService.ApiCnnAccuracyPerCategoryGet();
    const mobileNetAccuracy$: Observable<AccuracyPerCategoryModel> = this.accuracyService.ApiMobileNetV2AccuracyPerCategoryGet();
    const inceptionAccuracy$: Observable<AccuracyPerCategoryModel> = this.accuracyService.ApiInceptionResNetV2AccuracyPerCategoryGet();
  
    forkJoin([cnnAccuracy$, mobileNetAccuracy$, inceptionAccuracy$]).subscribe(
      ([cnnData, mobileNetData, inceptionData]) => {
        const seriesData = [
          {
            name: 'CNN Model',
            data: [
              cnnData.bags || 0,
              cnnData.bottomwear || 0,
              cnnData.dress || 0,
              cnnData.shoes || 0,
              cnnData.topwear || 0
            ],
          },
          {
            name: 'MobileNetV2 Model',
            data: [
              mobileNetData.bags || 0,
              mobileNetData.bottomwear || 0,
              mobileNetData.dress || 0,
              mobileNetData.shoes || 0,
              mobileNetData.topwear || 0
            ],
          },
          {
            name: 'InceptionResNetV2 Model',
            data: [
              inceptionData.bags || 0,
              inceptionData.bottomwear || 0,
              inceptionData.dress || 0,
              inceptionData.shoes || 0,
              inceptionData.topwear || 0
            ],
          }
        ];
        this.chartCategoryOptions.series = seriesData;
        this.cdr.detectChanges();
      },
      error => {
        console.error('Error fetching accuracy data:', error);
      }
    );
  }

  fetchAccuracyPerArticleTypeData() {
    const cnnAccuracy$: Observable<AccuracyPerArticleTypeModel> = this.accuracyService.ApiCnnAccuracyPerArticleTypeGet();
    const mobileNetAccuracy$: Observable<AccuracyPerArticleTypeModel> = this.accuracyService.ApiMobileNetV2AccuracyPerArticleTypeGet();
    const inceptionAccuracy$: Observable<AccuracyPerArticleTypeModel> = this.accuracyService.ApiInceptionResNetV2AccuracyPerArticleTypeGet();

    forkJoin([cnnAccuracy$, mobileNetAccuracy$, inceptionAccuracy$]).subscribe(
      ([cnnData, mobileNetData, inceptionData]) => {
        const seriesData = [
          {
            name: 'CNN Model',
            data: [
              cnnData.backpacks || 0,
              cnnData.capris || 0,
              cnnData.casual_shoes || 0,
              cnnData.clutches || 0,
              cnnData.dresses || 0,
              cnnData.flats || 0,
              cnnData.flip_flops || 0,
              cnnData.formal_shoes || 0,
              cnnData.handbags || 0,
              cnnData.heels || 0,
              cnnData.jackets || 0,
              cnnData.jeans || 0,
              cnnData.laptop_bag || 0,
              cnnData.leggings || 0,
              cnnData.sandals || 0,
              cnnData.shirts || 0,
              cnnData.shorts || 0,
              cnnData.skirts || 0,
              cnnData.sports_shoes || 0,
              cnnData.sweaters || 0,
              cnnData.tops || 0,
              cnnData.track_pants || 0,
              cnnData.trousers || 0,
              cnnData.tshirts || 0,
            ],
          },
          {
            name: 'MobileNetV2 Model',
            data: [
              mobileNetData.backpacks || 0,
              mobileNetData.capris || 0,
              mobileNetData.casual_shoes || 0,
              mobileNetData.clutches || 0,
              mobileNetData.dresses || 0,
              mobileNetData.flats || 0,
              mobileNetData.flip_flops || 0,
              mobileNetData.formal_shoes || 0,
              mobileNetData.handbags || 0,
              mobileNetData.heels || 0,
              mobileNetData.jackets || 0,
              mobileNetData.jeans || 0,
              mobileNetData.laptop_bag || 0,
              mobileNetData.leggings || 0,
              mobileNetData.sandals || 0,
              mobileNetData.shirts || 0,
              mobileNetData.shorts || 0,
              mobileNetData.skirts || 0,
              mobileNetData.sports_shoes || 0,
              mobileNetData.sweaters || 0,
              mobileNetData.tops || 0,
              mobileNetData.track_pants || 0,
              mobileNetData.trousers || 0,
              mobileNetData.tshirts || 0,
            ],
          },
          {
            name: 'InceptionResNetV2 Model',
            data: [
              inceptionData.backpacks || 0,
              inceptionData.capris || 0,
              inceptionData.casual_shoes || 0,
              inceptionData.clutches || 0,
              inceptionData.dresses || 0,
              inceptionData.flats || 0,
              inceptionData.flip_flops || 0,
              inceptionData.formal_shoes || 0,
              inceptionData.handbags || 0,
              inceptionData.heels || 0,
              inceptionData.jackets || 0,
              inceptionData.jeans || 0,
              inceptionData.laptop_bag || 0,
              inceptionData.leggings || 0,
              inceptionData.sandals || 0,
              inceptionData.shirts || 0,
              inceptionData.shorts || 0,
              inceptionData.skirts || 0,
              inceptionData.sports_shoes || 0,
              inceptionData.sweaters || 0,
              inceptionData.tops || 0,
              inceptionData.track_pants || 0,
              inceptionData.trousers || 0,
              inceptionData.tshirts || 0,
            ],
          }
        ];
        this.chartArticleTypeOptions.series = seriesData;
        this.cdr.detectChanges();
      },
      error => {
        console.error('Error fetching accuracy data:', error);
      }
    );
  }

  redrawCharts() {
    if (this.chart) {
      // Redraw Accuracy per Category chart
      this.chart.updateOptions(this.chartCategoryOptions);
      // Redraw Accuracy per Article Type chart
      this.chart.updateOptions(this.chartArticleTypeOptions);
    }
  }

  goToCNN(): void {
    this.router.navigate(['/cnn-model']);
  }

  goToMobileNetV2(): void {
    this.router.navigate(['/mobile-net-v2-model']);
  }

  goToInceptionResNetV2(): void {
    this.router.navigate(['/inception-res-net-v2-model']);
  }
}
