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
  selector: 'app-cnn-model',
  templateUrl: './cnn-model.component.html',
  styleUrl: './cnn-model.component.scss'
})
export class CnnModelComponent implements OnInit, AfterViewInit {
  @ViewChild("chart") chart!: ChartComponent | undefined;
  public chartCategoryOptions: Partial<ChartOptions> | any;
  public chartArticleTypeOptions: Partial<ChartOptions> | any;
  imageUrl: string | ArrayBuffer | null = null;
  public model: PredictionModel | null = null;
  public accuracyPerCategoryModel: AccuracyPerCategoryModel | null = null;
  public accuracyPerArticleTypeModel: AccuracyPerArticleTypeModel | null = null;
  selectedFileName: string | null = null;
  displayedColumns: string[] = ['predicted_category', 'confidence_category', 'predicted_article_type', 'confidence_article_type'];
  isLoading: boolean = false;

  constructor(
  private predictionService: PredictionService,
  private accuracyService: AccuracyService,
  private cdr: ChangeDetectorRef ) 
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
        "#4a148c5b",
        "#4a148c5b",
        "#4a148c5b",
        "#4a148c5b"
      ],
      plotOptions: {
        bar: {
          columnWidth: "30%",
          distributed: true
        }
      },
      dataLabels: {
        enabled: false
      },
      legend: {
        show: false
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
            colors: [
              "#6A1B9A",
              "#6A1B9A",
              "#6A1B9A",
              "#6A1B9A",
              "#6A1B9A"
            ],
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
        "#4a148c5b",
        "#4a148c5b",
        "#4a148c5b",
        "#4a148c5b",
        "#4a148c5b",
        "#4a148c5b",
        "#4a148c5b",
        "#4a148c5b",
        "#4a148c5b",
        "#4a148c5b",
        "#4a148c5b",
        "#4a148c5b",
        "#4a148c5b",
        "#4a148c5b",
        "#4a148c5b",
        "#4a148c5b",
        "#4a148c5b",
        "#4a148c5b",
        "#4a148c5b",
        "#4a148c5b",
        "#4a148c5b",
        "#4a148c5b",
        "#4a148c5b"
      ],
      plotOptions: {
        bar: {
          columnWidth: "30%",
          distributed: true
        }
      },
      dataLabels: {
        enabled: false
      },
      legend: {
        show: false
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
            colors: [
              "#6A1B9A",
              "#6A1B9A",
              "#6A1B9A",
              "#6A1B9A",
              "#6A1B9A",
              "#6A1B9A",
              "#6A1B9A",
              "#6A1B9A",
              "#6A1B9A",
              "#6A1B9A",
              "#6A1B9A",
              "#6A1B9A",
              "#6A1B9A",
              "#6A1B9A",
              "#6A1B9A",
              "#6A1B9A",
              "#6A1B9A",
              "#6A1B9A",
              "#6A1B9A",
              "#6A1B9A",
              "#6A1B9A",
              "#6A1B9A",
              "#6A1B9A",
              "#6A1B9A"
            ],
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

  onFileSelected(event: any) {
    const inputElement = event.target as HTMLInputElement;
    if (!inputElement || !inputElement.files || inputElement.files.length === 0) {
      console.error('No image selected');
      return;
    }
    
    const file: File = inputElement.files[0];
    this.selectedFileName = file.name;
    const reader = new FileReader();
    reader.readAsDataURL(file);
    reader.onload = () => {
      this.imageUrl = reader.result;
      this.model = null;
    };
  }

  onUpload(file: File) {
    if (!file) {
      console.error('No image selected');
      return;
    }
    
    this.isLoading = true;
    this.predictionService.ApiCnnPredictionPost(file).subscribe(
      response => {
        this.model = response;
        console.log('Prediction Result:', this.model);
        this.isLoading = false;
      },
      error => {
        console.error('Error:', error);
        this.isLoading = false;
      }
    );
  }
  
  fetchAccuracyPerCategoryData() {
    this.accuracyService.ApiCnnAccuracyPerCategoryGet().subscribe(
      (data: AccuracyPerCategoryModel) => {
        this.chartCategoryOptions.series = [
          {
            name: 'Accuracy',
            data: [
              data.bags || 0,
              data.bottomwear || 0,
              data.dress || 0,
              data.shoes || 0,
              data.topwear || 0
            ]
          }
        ];
        this.cdr.detectChanges();
      },
      error => {
        console.error('Error fetching accuracy data:', error);
      }
    );
  }

  fetchAccuracyPerArticleTypeData() {
    this.accuracyService.ApiCnnAccuracyPerArticleTypeGet().subscribe(
      (data: AccuracyPerArticleTypeModel) => {
        this.chartArticleTypeOptions.series = [
          {
            name: 'Accuracy',
            data: [
              data.backpacks || 0,
              data.capris || 0,
              data.casual_shoes || 0,
              data.clutches || 0,
              data.dresses || 0,
              data.flats || 0,
              data.flip_flops || 0,
              data.formal_shoes || 0,
              data.handbags || 0,
              data.heels || 0,
              data.jackets || 0,
              data.jeans || 0,
              data.laptop_bag || 0,
              data.leggings || 0,
              data.sandals || 0,
              data.shirts || 0,
              data.shorts || 0,
              data.skirts || 0,
              data.sports_shoes || 0,
              data.sweaters || 0,
              data.tops || 0,
              data.track_pants || 0,
              data.trousers || 0,
              data.tshirts || 0,
            ]
          }
        ];
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
}
