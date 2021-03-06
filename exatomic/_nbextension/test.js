// Copyright (c) 2015-2016, Exa Analytics Development Team
// Distributed under the terms of the Apache License 2.0
/*"""
test.js
####################
Test visualization application for the universe container (exatomic package).
*/
'use strict';


require.config({
    shim: {
        'nbextensions/exa/app3d': {
            exports: 'App3D'
        },
        'nbextensions/exa/gui': {
            exports: 'ContainerGUI'
        },
        'nbextensions/exa/num': {
            exports: 'num'
        },
        'nbextensions/exa/exatomic/ao': {
            exports: 'AO'
        },
        'nbextensions/exa/exatomic/gtf': {
            exports: 'GTF'
        },
        'nbextensions/exa/exatomic/gaussian': {
            exports: 'gaussian'
        },
        'nbextensions/exa/exatomic/harmonics': {
            exports: 'sh'
        },
    },
});


define([
    'nbextensions/exa/app3d',
    'nbextensions/exa/gui',
    'nbextensions/exa/num',
    'nbextensions/exa/exatomic/ao',
    'nbextensions/exa/exatomic/gtf',
    'nbextensions/exa/exatomic/gaussian',
    'nbextensions/exa/exatomic/harmonics'
], function(App3D, ContainerGUI, num, AO, GTF, gaussian, sh) {
    class UniverseTestApp {
        /*"""
        UniverseTestApp
        ==================
        A test application for the universe container (exatomic package).
        */
        constructor(view) {
            /*"""
            constructor
            --------------
            Args:
                view: Backbone.js view (DOMWidgetView container representation)
            */
            this.view = view;
            this.view.create_canvas();
            this.axis = [];
            this.active_objs = [];
            this.dimensions = {
                'ox': -25.0,  'oy': -25.0, 'oz': -25.0,
                'nx':  52,    'ny':  52,   'nz':  52,
                'dxi':  1.0, 'dxj':   0,   'dxk':  0,
                'dyi':  0,   'dyj':   1.0, 'dyk':  0,
                'dzi':  0,   'dzj':   0,   'dzk':  1.0
            };
            this.field = new AO(this.dimensions, '1s');
            this.app3d = new App3D(this.view.canvas);
            this.create_gui();
            this.axis = this.app3d.add_unit_axis();
            this.render_ao();
            this.ao.folder.open();
            this.app3d.set_camera({x: 5.5, y: 5.5, z: 5.5});
            this.view.container.append(this.gui.domElement);
            this.view.container.append(this.gui.custom_css);
            this.view.container.append(this.view.canvas);
            var view_self = this.view;
            this.view.on('displayed', function() {
                view_self.app.app3d.animate();
                view_self.app.app3d.controls.handleResize();
            });
        };

        create_gui() {
            /*"""
            create_gui
            --------------
            Creates the standard style container gui instance and populates
            with relevant controls for this application.
            */
            var self = this;
            self.return = false;
            this.gui = new ContainerGUI(this.view.gui_width);

            this.top = {
                /*
                'demo': 'Hydrogen Wave Functions',
                'demos': ['Hydrogen Wave Functions', 'Gaussian Type Functions', 'Cube', 'Trajectory'],
                'play': function() {
                    console.log('pushed play');
                },
                'fps': 24,
                */
                'save field': function() {
                    var field = {
                        'ox': self.field.xmin, 'oy': self.field.ymin, 'oz': self.field.zmin,
                        'dxi': self.field.dx, 'dyj': self.field.dy, 'dzk': self.field.dz,
                        'nx': self.field.nx, 'ny': self.field.ny, 'nz': self.field.nz,
                        'values': JSON.stringify(self.field.values),
                        'label': self.field.function
                    }
                    self.view.send({'type': 'field', 'data': field});
                },
                'save image': function() {
                    self.app3d.renderer.setSize(1920, 1080);
                    self.app3d.camera.aspect = 1920 / 1080;
                    self.app3d.camera.updateProjectionMatrix();
                    self.app3d.render();
                    var imgdat = self.app3d.renderer.domElement.toDataURL('image/png');
                    self.view.send({'type': 'image', 'data': imgdat});
                    self.app3d.renderer.setSize(self.app3d.width, self.app3d.height);
                    self.app3d.camera.aspect = self.app3d.width / self.app3d.height;
                    self.app3d.camera.updateProjectionMatrix();
                }
            };
            /*
            this.top['demo_dropdown'] = this.gui.add(this.top, 'demo', this.top['demos']);
            this.top['play_button'] = this.gui.add(this.top, 'play');
            this.top['fps_slider'] = this.gui.add(this.top, 'fps', 1, 60);
            */
            this.top['save_image'] = this.gui.add(this.top, 'save image');
            this.top['send_button'] = this.gui.add(this.top, 'save field');
            this.ao = {
                'function': '1s',
                'functions': ['1s', '2s', '2px', '2py', '2pz',
                              '3s', '3px', '3py', '3pz',
                              '3d-2', '3d-1', '3d0', '3d+1', '3d+2'],
                'isovalue': 0.005
            };
            this.ao['folder'] = this.gui.addFolder('Hydrogen Wave Functions');
            this.ao['func_dropdown'] = this.ao.folder.add(this.ao, 'function', this.ao['functions']);
            this.ao['isovalue_slider'] = this.ao.folder.add(this.ao, 'isovalue', 0.0, 0.4);
            this.ao['isovalue_slider'].onFinishChange(function(value) {
                self.ao['isovalue'] = value;
                self.render_ao();
            });
            this.ao['func_dropdown'].onFinishChange(function(value) {
                self.ao['function'] = value;
                self.render_ao();
            });

            this.gtf = {
                'function': 's',
                'functions': ['s', 'px', 'py', 'pz',
                              'd200', 'd110', 'd101', 'd020', 'd011', 'd002'],
                'isovalue': 0.005
            };
            this.gtf['folder'] = this.gui.addFolder('Gaussian Type Functions');
            this.gtf['func_dropdown'] = this.gtf.folder.add(this.gtf, 'function', this.gtf['functions']);
            this.gtf['isovalue_slider'] = this.gtf.folder.add(this.gtf, 'isovalue', 0.0, 0.4);
            this.gtf['isovalue_slider'].onFinishChange(function(value) {
                self.gtf['isovalue'] = value;
                self.render_gtf();
            });
            this.gtf['func_dropdown'].onFinishChange(function(value) {
                self.gtf['function'] = value;
                self.render_gtf();
            });

            this.sh = {'l': 0, 'm': 0, 'isovalue': 0.03};
            this.sh['folder'] = this.gui.addFolder('Solid Harmonics');
            //this.sh['isovalue_slider'] = this.sh.folder.add(this.sh, 'isovalue', 0.0001, 1.0);
            this.sh['l_slider'] = this.sh.folder.add(this.sh, 'l').min(0).max(7).step(1);
            this.sh['ml_slider'] = this.sh.folder.add(this.sh, 'm').min(0).max(0).step(1);
            /*
            this.sh['isovalue_slider'].onFinishChange(function(value) {
                self.sh['isovalue'] = value;
                self.render_solid_harmonic();
            });
            */
            this.sh.l_slider.onFinishChange(function(value) {
                self.sh.l = parseInt(value);
                self.update_m();
                self.render_solid_harmonic();
            });
        };

        update_m() {
            var self = this;
            this.sh.folder.__controllers[2].remove();
            this.sh.m = 0;
            if (this.sh.l === 0) {
                this.sh.m_slider = this.sh.folder.add(this.sh, 'm').min(0).max(0).step(1);
            } else {
                this.sh.m_slider = this.sh.folder.add(this.sh, 'm').min(-this.sh.l).max(this.sh.l).step(1);
            };
            this.sh.m_slider.onFinishChange(function(value) {
                self.sh.m = parseInt(value);
                self.render_solid_harmonic();
            });
        };

        render_solid_harmonic() {
            this.field = new sh.SolidHarmonic(this.sh.l, this.sh.m, this.dimensions);
            this.app3d.remove_meshes(this.active_objs);
            this.active_objs = this.app3d.add_scalar_field(this.field, this.sh.isovalue, 2);
        };

        render_ao() {
            this.field = new AO(this.dimensions, this.ao['function']);
            this.app3d.remove_meshes(this.active_objs);
            this.active_objs = this.app3d.add_scalar_field(this.field, this.ao.isovalue, 2);
        };

        render_gtf() {
            this.field = new GTF(this.dimensions, this.gtf['function']);
            this.app3d.remove_meshes(this.active_objs);
            this.active_objs = this.app3d.add_scalar_field(this.field, this.gtf.isovalue, 2);
        };

        resize() {
            this.app3d.resize();
        };
    };


    return UniverseTestApp;
});
