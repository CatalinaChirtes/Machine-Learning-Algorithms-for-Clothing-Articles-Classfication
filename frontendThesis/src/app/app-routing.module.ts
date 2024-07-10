import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { MainComponent } from './main/main.component';
import { PageNotFoundComponent } from './page-not-found/page-not-found.component';
import { CnnModelComponent } from './main/cnn-model/cnn-model.component';
import { MobileNetV2ModelComponent } from './main/mobile-net-v2-model/mobile-net-v2-model.component';
import { InceptionResNetV2ModelComponent } from './main/inception-res-net-v2-model/inception-res-net-v2-model.component';
import { HomePageComponent } from './main/home-page/home-page.component';

const routes: Routes = [
  {
    path: '',
    component: MainComponent,
    children: [
      {
        path: '',
        redirectTo: '/home-page',
        pathMatch: 'full'
      },
      {
        path: 'home-page',
        component: HomePageComponent
      },
      {
        path: 'cnn-model',
        component: CnnModelComponent
      },
      {
        path: 'mobile-net-v2-model',
        component: MobileNetV2ModelComponent
      },
      {
        path: 'inception-res-net-v2-model',
        component: InceptionResNetV2ModelComponent
      },
    ]
  },
  {
    path: '**',
    component: PageNotFoundComponent
  }
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
