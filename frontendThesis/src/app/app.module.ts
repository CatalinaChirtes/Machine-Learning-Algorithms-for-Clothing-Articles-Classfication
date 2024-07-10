import { NgModule } from '@angular/core';

// MODULES
import { BrowserModule } from '@angular/platform-browser';
import { AppRoutingModule } from './app-routing.module';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { HttpClient, HttpClientModule, HTTP_INTERCEPTORS } from '@angular/common/http';

// MATERIAL
import { MaterialModule } from './material.module';

// PLUGINS
import { QuillModule } from 'ngx-quill';
import { TranslateLoader, TranslateModule } from '@ngx-translate/core';
import { TranslateHttpLoader } from '@ngx-translate/http-loader';

// ENVIRONMENT
import { environment } from '../environments/environment';

// COMPONENTS
import { AppComponent } from './app.component';
import { MainComponent } from './main/main.component';
import { SidenavComponent } from './shared/components/sidenav/sidenav.component';
import { ToolbarComponent } from './shared/components/toolbar/toolbar.component';
import { CnnModelComponent } from './main/cnn-model/cnn-model.component';
import { PageNotFoundComponent } from './page-not-found/page-not-found.component';
import { MobileNetV2ModelComponent } from './main/mobile-net-v2-model/mobile-net-v2-model.component';
import { NgApexchartsModule } from 'ng-apexcharts';
import { InceptionResNetV2ModelComponent } from './main/inception-res-net-v2-model/inception-res-net-v2-model.component';
import { HomePageComponent } from './main/home-page/home-page.component';


export function HttpLoaderFactory(http: HttpClient) {
  return new TranslateHttpLoader(http);
}

@NgModule({
  declarations: [
    AppComponent,
    MainComponent,
    CnnModelComponent,
    MobileNetV2ModelComponent,
    InceptionResNetV2ModelComponent,
    HomePageComponent,
    PageNotFoundComponent,
    SidenavComponent,
    ToolbarComponent,
  ],
  imports: [
  BrowserModule,
    ReactiveFormsModule,
    AppRoutingModule,
    BrowserAnimationsModule,
    FormsModule,
    HttpClientModule,
    MaterialModule,
    NgApexchartsModule,
    QuillModule.forRoot(),
    TranslateModule.forRoot({
      defaultLanguage: environment.defaultLang,
      loader: {
        provide: TranslateLoader,
        useFactory: HttpLoaderFactory,
        deps: [HttpClient]
      }
    }),
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule {}
