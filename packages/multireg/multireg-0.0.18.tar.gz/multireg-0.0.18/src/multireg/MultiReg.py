import napari
import tifffile
from magicgui import magicgui
from napari.utils.notifications import show_info
import itk
import random
import numpy as np
import pathlib
import os, glob
import multireg.Utils as ut
from qtpy.QtWidgets import QFileDialog
from napari.utils.history import get_save_history, update_save_history
from webbrowser import open_new_tab


def get_filename():
    dialog = QFileDialog(caption="Choose reference image")
    hist = get_save_history()
    dialog.setHistory(hist)
    dialog.setFileMode(QFileDialog.ExistingFile)
    dialog.setDirectory(hist[0])
    if dialog.exec_():
        filename = dialog.selectedFiles()
    if filename:
        return filename[0]
    else:
        return None

def start():
    global viewer, aligndir, imagedir
    global refimg, refchanel
    global imagename
    global scaleXY, scaleZ
    refchanel = 0
    viewer = napari.current_viewer()
    viewer.title = "MultiReg"
    filename = get_filename()
    if filename is None:
        print("No file selected")
        return
    refimg, scaleXY, scaleZ, names = ut.open_image(filename, verbose=True)
    imagename, imagedir, aligndir = ut.extract_names( filename, subname="aligned" )
    update_save_history(imagedir)
    for chan in range(refimg.shape[0]):
        cmap = ut.colormapname(chan)
        viewer.add_image( refimg[chan,], name="fixedImg_"+"C"+str(chan), blending="additive", colormap = cmap )
    return getChanels()

def getChanels():

    def open_doc():
        open_new_tab("https://gitlab.pasteur.fr/gletort/multireg#fixed-image")

    @magicgui(call_button="Update", 
            reference_chanel={"widget_type": "Slider", "min":0, "max": refimg.shape[0]-1}, 
            Help={"widget_type":"PushButton", "value": False},
            )
    def get_chanel( reference_chanel=0 , Help=False):
        global refchanel
        viewer.window.remove_dock_widget("all")
        refchanel = reference_chanel
        for chan in range(refimg.shape[0]):
            layname = "fixedImg_"+"C"+str(chan)
            if chan != refchanel:
                if layname in viewer.layers:
                    viewer.layers.remove(layname)
            else:
                if layname not in viewer.layers: 
                    viewer.add_image( refimg[chan,], name=layname, blending="additive", colormap = "red" )
                else:
                    viewer.layers[layname].colormap = "red"
            ut.writeTif( refimg[chan,], os.path.join(aligndir,imagename+"_C"+str(chan)+".tif"), scaleXY, scaleZ, "uint16" )
        if "Place reference points" not in viewer.window._dock_widgets:
            reference_points()
    
    get_chanel.Help.clicked.connect(open_doc)
    wid = viewer.window.add_dock_widget(get_chanel, name="Choose chanel")
    return wid


def load_images():
    @magicgui( call_button="All done",
            #do_moving_image={"widget_type":"PushButton", "value": False},
            )
    def end_images( moving_img = pathlib.Path(imagedir), 
            #do_moving_image=False
            ):
        create_result_image()

    def go_image():
        moving_img = end_images.moving_img.value
        global results_transform_parameters_aff, results_transform_parameters
        global movname
        global movimg
        results_transform_parameters_aff = None
        results_transform_parameters = None
    
        movimg, scaleXY, scaleZ, names = ut.open_image(moving_img, verbose=True)
        movname, idir, adir = ut.extract_names( moving_img, subname="aligned" )
        movname = os.path.splitext(movname)[0]
       
        # open images as itk files
        viewer.add_image( movimg[refchanel,], name="movingImg_C"+str(refchanel), blending="additive", colormap = "green" )
        moving_points()

    #end_images.do_moving_image.clicked.connect(go_image)
    end_images.moving_img.changed.connect(go_image)
    wid = viewer.window.add_dock_widget(end_images, name="Do Image")
    return wid

def itk_to_layer(img, name, color):
    lay = layer_from_image(img)
    lay.blending = "additive"
    lay.colormap = color
    lay.name = name
    viewer.add_layer( lay )

def reference_points(npts=2):
    """ Initialize with randomly placed points on the reference image """
    ptsfi = []
    labels = []
    fisize = viewer.layers["fixedImg"+"_C"+str(refchanel)].level_shapes[0]
    ## initialize with randomly placed points
    for pt in range(npts):
        ptx = random.random()*fisize[1]
        pty = random.random()*fisize[2]
        ptz = random.random()*fisize[0]
        ptsfi.append([ptz,ptx,pty])
        labels.append(pt)
    col = np.array( [1, 0.3, 0.5] )
    add_points(ptsfi, labels, col, "fixedPoints")
   
    ## widget to load/save point file/update points
    @magicgui(call_button="Fixed points done",
            load_points={"widget_type":"PushButton", "value": False},
            To_edit={"widget_type":"Label"},
            selected_point_label={"widget_type":"LineEdit"},
            set_label={"widget_type":"PushButton", "value": False},
            save_points={"widget_type":"PushButton", "value": False},
            help={"widget_type":"PushButton", "value": False},
            )
    def do_points(
            load_fixed=pathlib.Path(os.path.join(aligndir, imagename+"_points.txt")),
            load_points=False, 
            To_edit="Select a point ('3') \n Press 'u' or 'd' to move it up or down \n Change its label below:",
            selected_point_label=0,
            set_label = False,
            save_points = False,
            help = False, 
            ):
        remove_widget("Fixed points")
        if "Do Image" not in viewer.window._dock_widgets:
            load_images()
        return
    
    def open_doc():
        open_new_tab("https://gitlab.pasteur.fr/gletort/multireg#reference-points")
    
    def save_refpoints():
        save_points_file(imagename, "fixedPoints")

    def set_point_label():
        layer = viewer.layers.selection.active
        sel = layer.selected_data
        for ind in sel:
            #layer.features["label"][ind] = int(do_points.selected_point_label.value)
            layer.features.loc[ind, "label"] = int(do_points.selected_point_label.value)
        layer.refresh()
        layer.refresh_text()

    @viewer.bind_key('u', overwrite=True)
    def move_point_up_inz(viewer):
        layer = viewer.layers.selection.active
        sel = layer.selected_data
        for ind in sel:
            z = layer.data[ind][0]
            if z < (fisize[0]-1):
                layer.data[ind][0] = z + 1
                viewer.dims.set_point(0, z+1)
        layer.refresh()
        layer.refresh_text()

    @viewer.bind_key('d', overwrite=True)
    def move_point_down_inz(viewer):
        layer = viewer.layers.selection.active
        sel = layer.selected_data
        for ind in sel:
            z = layer.data[ind][0]
            if z > 0:
                layer.data[ind][0] = z - 1
                viewer.dims.set_point(0, z-1)
        layer.refresh()
        layer.refresh_text()


    def load_points_from_file():
        """ Load the fixed points from file """
        fixedfile = do_points.load_fixed.value
        col = np.array( [1, 0.3, 0.6] )
        load_points_file(fixedfile, "fixedPoints", col )

    do_points.load_points.clicked.connect(load_points_from_file)
    do_points.set_label.clicked.connect(set_point_label)
    do_points.save_points.clicked.connect(save_refpoints)
    do_points.help.clicked.connect(open_doc)
    wid = viewer.window.add_dock_widget(do_points, name="Fixed points")
    return wid


def moving_points():
    """ Get (place, load, update) the moving points """
    ptsmo = []
    labels = []
    new_view = None
    points_fixed = viewer.layers["fixedPoints"]
    npoints_fixed = len( points_fixed.data )
    fisize = viewer.layers["fixedImg"+"_C"+str(refchanel)].level_shapes[0]
    labs = points_fixed.features["label"]
    ## initialize with points close to the reference points
    #for pt, lab in zip(points_fixed.data, labs):
    #    ptx = pt[1]*0.8
    #    pty = pt[2]*0.8
    #    ptz = pt[0] 
    #    ptsmo.append([ptz,ptx,pty])
    #    labels.append(lab)
    col = np.array( [0.3, 1, 0.6] )
    add_points(ptsmo, labels, col, "movingPoints")
    
    @magicgui(call_button="Moving points done",
            _={"widget_type":"Label"},
            load_points={"widget_type":"PushButton", "value": False},
            To_edit={"widget_type":"Label"},
            selected_point_label={"widget_type":"LineEdit"},
            set_label={"widget_type":"PushButton", "value": False},
            save_points={"widget_type":"PushButton", "value": False},
            Help={"widget_type":"PushButton", "value": False},
            )
    def do_points(
            _ = "Place the "+str(npoints_fixed)+" points on moving image\n(corresponding to ref points)",
            load_moving=pathlib.Path(os.path.join(aligndir, movname+"_points.txt")),
            load_points=False, 
            side_by_side_view=False, 
            two_windows_view=False, 
            To_edit="Select a point ('3') \n Press 'u' or 'd' to move it up or down \n Change its label below:",
            selected_point_label=0,
            set_label = False,
            save_points = False,
            Help = False,
            ):
        if "Moving points" in viewer.window._dock_widgets:
            if new_view is not None:
                try:
                    new_view.close();
                except: 
                    print("Window already closed")
            remove_widget("Moving points")
            viewer.grid.enabled = False
        calc_alignement()
        return
    
    def open_doc():
        open_new_tab("https://gitlab.pasteur.fr/gletort/multireg#moving-points")

    def save_points():
        save_points_file(movname, "movingPoints")

    def side_view():
        if do_points.side_by_side_view.value:
            lays = viewer.layers
            ind = lays.index(lays["fixedImg"+"_C"+str(refchanel)])
            if ind != 0:
                lays.move(ind,0)
            indpt = lays.index(lays["fixedPoints"])
            if indpt != 1:
                lays.move(indpt,1)
            ind = lays.index(lays["movingImg"+"_C"+str(refchanel)])
            if ind != 2:
                lays.move(ind,2)
            indpt = lays.index(lays["movingPoints"])
            if indpt != 3:
                lays.move(indpt,3)
            viewer.grid.enabled = True
            viewer.grid.stride = 2    
        else:
            viewer.grid.enabled = False
    
    def windows_view():
        nonlocal new_view
        if do_points.two_windows_view.value:
            lays = viewer.layers
            new_view = napari.Viewer()

            fixed_img = lays["fixedImg_C"+str(refchanel)]
            copy_fixed = new_view.add_image(fixed_img.data.copy())
            copy_fixed.name = "fixedImg"
            copy_fixed.colormap = "red"
            fixed_img.visible = False

            fixed_pts = lays["fixedPoints"]
            col = np.array( [1, 0.3, 0.6] )
            copy_fixed_pts = new_view.add_points( fixed_pts.data.copy(), properties=fixed_pts.properties.copy(), face_color=col, size = 28, text='label', edge_width=0, name="fixedPts", )
            copy_fixed_pts.text.color = col
            copy_fixed_pts.text.size = 24
            copy_fixed_pts.text.anchor = "upper_left"
            #copy_fixed_pts.text.translation = np.array([0, -18,18])
            fixed_pts.visible = False

        else:
            if new_view is not None:
                try:
                    new_view.close()
                except: 
                    print("Window already closed")


    def set_point_label():
        layer = viewer.layers.selection.active
        sel = layer.selected_data
        for ind in sel:
            #layer.features["label"][ind] = int(do_points.selected_point_label.value)
            layer.features.loc[ind, "label"] = int(do_points.selected_point_label.value)
        layer.refresh()
        layer.refresh_text()

    def load_points_from_file():
        movefile = do_points.load_moving.value
        col = np.array( [0.3, 1, 0.6] )
        load_points_file(movefile, "movingPoints", col )
        side_view()
    
    @viewer.bind_key('u', overwrite=True)
    def move_point_up_inz(viewer):
        layer = viewer.layers.selection.active
        sel = layer.selected_data
        for ind in sel:
            z = layer.data[ind][0]
            if z < (fisize[0]-1):
                layer.data[ind][0] = z + 1
                viewer.dims.set_point(0, z+1)
        layer.refresh()
        layer.refresh_text()

    @viewer.bind_key('d', overwrite=True)
    def move_point_down_inz(viewer):
        layer = viewer.layers.selection.active
        sel = layer.selected_data
        for ind in sel:
            z = layer.data[ind][0]
            if z > 0:
                layer.data[ind][0] = z - 1
                viewer.dims.set_point(0, z-1)
        layer.refresh()
        layer.refresh_text()


    do_points.load_points.clicked.connect(load_points_from_file)
    do_points.set_label.clicked.connect(set_point_label)
    do_points.side_by_side_view.changed.connect(side_view)
    do_points.two_windows_view.changed.connect(windows_view)
    do_points.save_points.clicked.connect(save_points)
    do_points.Help.clicked.connect(open_doc)
    wid = viewer.window.add_dock_widget(do_points, name="Moving points")
    return wid

def add_points(pts, labels, color, name):
    features = {"label": np.array(labels, dtype="int") }
    points = viewer.add_points( np.array(pts), properties=features, face_color=color, size = 28, text='label', edge_width=0, name=name, )
    points.text.color = color
    points.text.size = 24
    #points.text.translation = np.array([0, -18,18])
    points.text.anchor = "upper_left"
    points.feature_defaults["label"] = len( pts )
    napari_add = points.add
    def add_with_label( coord ):
        ## for the new label when adding manually a point
        points.feature_defaults["label"] = len( points.data )
        napari_add( coord )
    points.add = add_with_label



def calc_alignement():
    def open_doc():
        open_new_tab("https://gitlab.pasteur.fr/gletort/multireg#alignement-calculation")

    @magicgui(call_button="Go", 
            max_step_length={"widget_type":"LiteralEvalLineEdit"}, 
            resolution={"widget_type":"LiteralEvalLineEdit"}, 
            iterations={"widget_type":"LiteralEvalLineEdit"}, 
            final_spacing={"widget_type":"LiteralEvalLineEdit"}, 
            spacing_one={"widget_type":"LiteralEvalLineEdit"}, 
            spacing_two={"widget_type":"LiteralEvalLineEdit"}, 
            spacing_three={"widget_type":"LiteralEvalLineEdit"}, 
            spacing_four={"widget_type":"LiteralEvalLineEdit"}, 
            Help={"widget_type":"PushButton", "value": False},
            )
    def get_paras( show_log = True,
            do_rigid = True,
            do_bspline = True,
            use_reference_points = True,
            strong_weight_on_points = True,
            show_advanced_parameters = False,
            show_intermediate_layer = False,
            resolution=4,
            max_step_length = 3,
            iterations=1000,
            final_spacing=50, 
            spacing_one=8,
            spacing_two=4,
            spacing_three=2,
            spacing_four=1,
            Help=False,
            ):
        
        global results_transform_parameters_aff, results_transform_parameters
        movlay = viewer.layers["movingImg_C"+str(refchanel)]
        fixlay = viewer.layers["fixedImg"+"_C"+str(refchanel)]
        results_transform_para_aff = None
        
        fimage = itk.image_view_from_array(fixlay.data)
        fimage = fimage.astype(itk.F)
        mimage = itk.image_view_from_array(movlay.data)
        mimage = mimage.astype(itk.F)
        affimage = mimage 

        if do_rigid:
            parameter_object = None
            parameter_object = itk.ParameterObject.New()
            parameter_map_rigid = parameter_object.GetDefaultParameterMap('rigid')
            parameter_map_rigid['MaximumNumberOfIterations'] = [str(iterations)]
            parameter_map_rigid['MaximumStepLength'] = [str(max_step_length)]
            parameter_map_rigid["NumberOfResolutions"] = [str(resolution)]
            parameter_map_rigid['NumberOfSpatialSamples'] = ['4000']
            parameter_map_rigid['MaximumNumberOfSamplingAttempts'] = ['8']
            parameter_map_rigid['RequiredRatioOfValidSamples'] = ['0.05']
            parameter_map_rigid['CheckNumberOfSamples'] = ['false']
            parameter_map_rigid['FinalGridSpacingInPhysicalUnits'] = [str(final_spacing)]
            parameter_map_rigid['Registration'] = ['MultiMetricMultiResolutionRegistration']
            parameter_map_rigid["AutomaticTransformInitialization"] = ['true']
            parameter_map_rigid["AutomaticTransformInitializationMethod"] = ['CenterOfGravity']
            gridspace = [str(spacing_one*4)]
            if resolution > 1:
                gridspace.append(str(spacing_two*2))
            if resolution > 2:
                gridspace.append(str(spacing_three*2))
            if resolution > 3:
                gridspace.append(str(spacing_four*1))
            if resolution > 4:
                gridspace.append(str(int(spacing_four)))
            parameter_map_rigid['GridSpacingSchedule'] = gridspace
            original_metric = parameter_map_rigid['Metric']
            if use_reference_points:
                parameter_map_rigid['Metric'] = [original_metric[0], 'CorrespondingPointsEuclideanDistanceMetric']
                if strong_weight_on_points:
                    parameter_map_rigid["Metric0Weight"] = ["0.2"]
                    parameter_map_rigid["Metric1Weight"] = ["0.8"]

            parameter_object.AddParameterMap(parameter_map_rigid)
        
            elastix_object = None
            elastix_object = itk.ElastixRegistrationMethod.New(fimage, mimage)
            elastix_object.SetParameterObject(parameter_object)
            
            if use_reference_points:
                elastix_object.SetFixedPointSetFileName(os.path.join(aligndir, imagename+"_points.txt"))
                elastix_object.SetMovingPointSetFileName(os.path.join(aligndir, movname+"_points.txt"))
            
            # Set additional options
            elastix_object.SetLogToConsole(show_log)

            # Update filter object (required)
            elastix_object.UpdateLargestPossibleRegion()

            # Results of Registration
            affimage = elastix_object.GetOutput()
            results_transform_parameters_aff = elastix_object.GetTransformParameterObject()
            
            # Show intermediate layer
            if show_intermediate_layer:
                resimage = affimage
                resclayer = layer_from_image(resimage)
                resclayer.blending = "additive"
                resclayer.name = "AfterAffineRegistration"
                viewer.add_layer( resclayer )
        
        # first rigid transformation
        if do_bspline:
            parameter_object = None
            elastix_object = None
            preset = "bspline"
            parameter_object = itk.ParameterObject.New()
            parameter_map = parameter_object.GetDefaultParameterMap(preset)
            parameter_map["NumberOfResolutions"] = [str(resolution)]
            parameter_map["WriteIterationInfo"] = ["false"]
            parameter_map['MaximumStepLength'] = [str(max_step_length)]
            parameter_map['NumberOfSpatialSamples'] = ['20000']
            parameter_map['MaximumNumberOfSamplingAttempts'] = ['10']
            parameter_map['RequiredRatioOfValidSamples'] = ['0.05']
            parameter_map['MaximumNumberOfIterations'] = [str(iterations)]
            parameter_map['FinalGridSpacingInPhysicalUnits'] = [str(final_spacing)]
            parameter_map['FinalBSplineInterpolationOrder'] = [str(3)]
            parameter_map['BSplineInterpolationOrder'] = [str(3)]
            parameter_map['HowToCombineTransform'] = ['Compose']
            gridspace = [str(spacing_one)]
            if resolution > 1:
                gridspace.append(str(spacing_two))
            if resolution > 2:
                gridspace.append(str(spacing_three))
            if resolution > 3:
                gridspace.append(str(spacing_four))
            if resolution > 4:
                gridspace.append(str(int(spacing_four/2)))
            parameter_map['GridSpacingSchedule'] = gridspace
            if not do_rigid and use_reference_points:
                original_metric = parameter_map['Metric']
                parameter_map['Metric'] = [original_metric[0], 'CorrespondingPointsEuclideanDistanceMetric']
                if strong_weight_on_points:
                    parameter_map["Metric0Weight"] = ["0.2"]
                    parameter_map["Metric1Weight"] = ["0.8"]
            parameter_object.AddParameterMap(parameter_map)
    
            # Load Elastix Image Filter Object
            elastix_object = itk.ElastixRegistrationMethod.New(fimage, affimage)
            elastix_object.SetParameterObject(parameter_object)
        
            if not do_rigid and use_reference_points:
                elastix_object.SetFixedPointSetFileName(os.path.join(aligndir, imagename+"_points.txt"))
                elastix_object.SetMovingPointSetFileName(os.path.join(aligndir, movname+"_points.txt"))
            # Set additional options
            elastix_object.SetLogToConsole(show_log)

            # Update filter object (required)
            elastix_object.UpdateLargestPossibleRegion()

        # Results of Registration
        result_image = elastix_object.GetOutput()
        results_transform_parameters = elastix_object.GetTransformParameterObject()

        reslayerbs = layer_from_image(result_image)
        reslayerbs.blending="additive"
        reslayerbs.name = "alignedMovingImg"
        viewer.add_layer( reslayerbs )
            
        movlay.visible = False
        apply_transformations()

    
    def show_advanced(booly):
        get_paras.show_intermediate_layer.visible = booly
        get_paras.resolution.visible = booly
        get_paras.max_step_length.visible = booly
        get_paras.iterations.visible = booly
        get_paras.final_spacing.visible = booly
        get_paras.spacing_one.visible = booly
        get_paras.spacing_two.visible = booly
        get_paras.spacing_three.visible = booly
        get_paras.spacing_four.visible = booly

    show_advanced(False)
    get_paras.show_advanced_parameters.changed.connect(show_advanced)
    get_paras.Help.clicked.connect(open_doc)
    wid = viewer.window.add_dock_widget(get_paras, name="Calculate alignement")
    return wid
        

def layer_from_image(img):
    data = np.array(itk.array_view_from_image(img))
    image_layer = napari.layers.Image(data)
    return image_layer


def point_set_from_txt(file_path, namePts, imsize=None):
    ind = 0 
    pts = []
    labels = []
    with open(file_path, "rt") as myfile:
        for myline in myfile:
            string = myline.partition('OutputPoint =')[2]
            string=string.strip()
            string = string.partition(']')[0]
            string = string.strip('[]')
            string=string.strip()
            x,y = string.split()
            #pts.append([float(x), float(y)])
            if imsize is not None:
                y = imsize - float(y)
            pts.append([float(y), float(x)])
            labels.append(ind)
            ind = ind + 1
    
    features = {"label":np.array(labels)}
    col = np.array( [0.3, 1, 0.7] )
    text = { 'string':'{label}',
                'size': 24,
                'color': col,
                'anchor': 'upper_left',
                #'translation': np.array([0, -5, 0]),
    }

    points_created = viewer.add_points( np.array(pts), features=features, face_color="blue", size = 28, text=text, edge_width=0, name=namePts )
    return pts

def write_point_set_to_txt(pts, labs, filepath, imsize=None):
    f = open(filepath, "w")
    f.write("index\n")
    f.write(str(len(pts))+"\n")
    order = np.argsort(labs)
    for ind in order:
        pt = pts[ind]
        y = pt[1]
        if imsize is not None:
            y = imsize - pt[1]
        f.write(str(pt[2])+" "+str(y)+" "+str(pt[0])+"\n")
        #f.write(str(y)+" "+str(pt[1])+"\n")
    f.close()

def apply_transformations():
    chanellist = list(range(movimg.shape[0]))
    
    def open_doc():
        open_new_tab("https://gitlab.pasteur.fr/gletort/multireg#apply-alignement")
    
    @magicgui(call_button="Align images",
            align_chanels=dict(widget_type="Select", choices=chanellist),
            Help={"widget_type":"PushButton", "value": False},
            )
    def apply_done(align_chanels=chanellist, Help=False):
        print("apply alignment to "+str(align_chanels))
        remove_widget("Calculate alignement")
        for chan in align_chanels:
            img = movimg[chan,]
            res = []
            itkimage = itk.image_view_from_array(img)
            itkimage = itkimage.astype(itk.F)
            ImageType = itk.Image[itk.F, 3]
            if results_transform_parameters_aff is not None:
                transformix_filter = itk.TransformixFilter[ImageType].New()
                transformix_filter.SetMovingImage(itkimage)
                transformix_filter.SetTransformParameterObject(results_transform_parameters_aff)
                aff_image = transformix_filter.GetOutput()
            else:
                aff_image = image
        
            if results_transform_parameters is not None:
                transformix = itk.TransformixFilter[ImageType].New()
                transformix.SetMovingImage(aff_image)
                transformix.SetTransformParameterObject(results_transform_parameters)
                res_image = transformix.GetOutput()
            else:
                res_image = aff_image

            res = itk.array_from_image(res_image)
            res[res<0] = 0
            res = np.array(res)
            ut.writeTif( res, os.path.join(aligndir, movname+"_C"+str(chan)+".tif"), scaleXY, scaleZ, "uint16" )
            
        finish_image()

    apply_done.Help.clicked.connect(open_doc)
    viewer.window.add_dock_widget(apply_done, name="Apply alignement")
    return

def finish_image():
    global movimg
    remove_widget("Calculate alignement")
    remove_layer("movingPoints")
    remove_layer("movingImg"+"_C"+str(refchanel))
    #for chan in range(movimg.shape[0]):
    #    remove_layer("imageAligned"+str(chan))
    remove_layer("alignedMovingImg")
    del movimg
    remove_widget("Apply alignement")

def remove_layer(layname):
    if layname in viewer.layers:
        viewer.layers.remove(layname)

def save_points_file(imname, layname):
    points_fixed = viewer.layers[layname]
    fpoints = points_fixed.data
    labs = points_fixed.features["label"]
    write_point_set_to_txt(fpoints, labs, os.path.join(aligndir, imname+"_points.txt"), None)

def load_points_file(ptfile, ptlayname, color):
    pts = []
    if os.path.exists(ptfile):
        viewer.layers.remove(ptlayname)
        labels = []
        with open(ptfile, 'r') as f:
            lines = f.readlines()
            ind = 0
            for line in lines:
                if ind >= 2:
                    pt = line.split(" ") 
                    ptz = float(pt[2])
                    ptx = float(pt[1])
                    pty = float(pt[0])
                    pts.append([int(ptz), int(ptx), int(pty)])
                    labels.append(ind-2)
                ind = ind + 1
        add_points(pts, labels, color, ptlayname)
        show_info("Loaded "+str(len(pts))+" points")

def remove_widget(widname):
    if widname in viewer.window._dock_widgets:
        wid = viewer.window._dock_widgets[widname]
        wid.setDisabled(True)
        del viewer.window._dock_widgets[widname]
        wid.destroyOnClose()

def create_result_image():
    allist = sorted(glob.glob(os.path.join(aligndir, "*_C*.tif")))
    allist = [os.path.basename(ref) for ref in allist]
    reflist = sorted(glob.glob(os.path.join(aligndir, "*_C"+str(refchanel)+".tif")))
    reflist = [os.path.basename(ref) for ref in reflist]
    filelist = sorted(glob.glob(os.path.join(aligndir, "*_C"+"[!"+str(refchanel)+"].tif")))
    filelist = [os.path.basename(chanfile) for chanfile in filelist]
    remove_widget("Do Image")
    
    @magicgui(call_button = "Create Image",
            average_chanels = dict(widget_type="Select", choices=allist), 
            add_chanels = dict(widget_type="Select", choices=allist), )
    def get_files(average_chanels=reflist, add_chanels=filelist, delete_files=True):
        resimg = np.zeros((len(add_chanels)+1,)+refimg.shape[1:]) 
        ind = 0
        for refchan in average_chanels:
            img, tscaleXY, tscaleZ, names = ut.open_image(os.path.join(aligndir,refchan), verbose=False)
            resimg[ind,] = resimg[ind,] + img
            if delete_files:
                os.remove(os.path.join(aligndir,refchan))
        resimg = resimg/len(average_chanels)

        ind = 1
        for chan in add_chanels:
            img, tscaleXY, tscaleZ, names = ut.open_image(os.path.join(aligndir,chan), verbose=False)
            resimg[ind,] = img
            ind = ind + 1
            if delete_files:
                os.remove(os.path.join(aligndir,chan))

        viewer.add_image(resimg, name="Res", blending="additive")
        for lay in viewer.layers:
            if lay.name != "Res":
                remove_layer(lay)
        imgname = os.path.join(aligndir, imagename+".tif")
        resimg = np.array(resimg, "uint16")
        # move the chanel axis after the Z axis (imageJ format)
        resimg = np.moveaxis(resimg, 0, 1)
        tifffile.imwrite(imgname, resimg, imagej=True, resolution=[1./scaleXY, 1./scaleXY], metadata={'PhysicalSizeX': scaleXY, 'spacing': scaleZ, 'unit': 'um', 'axes': 'ZCYX'})
        show_info("Image "+imgname+" saved")
        remove_widget("Choose chanels")
    
    viewer.window.add_dock_widget(get_files, name="Choose chanels")
