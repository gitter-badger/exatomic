/*"""
=========================================================
Universe View
=========================================================
*/
'use strict';


require.config({
    shim: {
        'nbextensions/exa/container': {
            exports: 'base'
        },

        'nbextensions/exa/atomic/app': {
            exports: 'UniverseApp'
        },

        'nbextensions/exa/atomic/test': {
            exports: 'UniverseTestApp'
        },
    },
});


define([
    'nbextensions/exa/container',
    'nbextensions/exa/atomic/test',
    'nbextensions/exa/atomic/app'
], function(base, UniverseTestApp, UniverseApp) {
    class UniverseView extends base.ContainerView {
        /*"""
        UniverseView
        ================
        */
        init() {
            this.init_listeners();
            this.if_empty();
        };

        if_empty() {
            /*"""
            if_empty
            ----------
            Create a UniverseTestApp application?
            */
            var check = this.get_trait('test');
            if (check === true) {
                console.log('Empty universe, displaying test interface!');
                this.app = new UniverseTestApp(this);
            } else {
                this.app = new UniverseApp(this);
            };
        };

        init_listeners() {
            /*"""
            init_listeners
            ---------------
            Set up the frontend to listen for changes on the backend
            */
            // Frame
            this.get_framelist();
            this.get_frame_ox();
            this.get_frame_oy();
            this.get_frame_oz();
            this.get_frame_xi();
            this.get_frame_xj();
            this.get_frame_xk();
            this.get_frame_yi();
            this.get_frame_yj();
            this.get_frame_yk();
            this.get_frame_zi();
            this.get_frame_zj();
            this.get_frame_zk();
            this.model.on('change:frame_frame', this.get_framelist, this);
            this.model.on('change:frame_ox', this.get_frame_ox, this);
            this.model.on('change:frame_oy', this.get_frame_ox, this);
            this.model.on('change:frame_oz', this.get_frame_ox, this);
            this.model.on('change:frame_xi', this.get_frame_ox, this);
            this.model.on('change:frame_xj', this.get_frame_ox, this);
            this.model.on('change:frame_xk', this.get_frame_ox, this);
            this.model.on('change:frame_yi', this.get_frame_ox, this);
            this.model.on('change:frame_yj', this.get_frame_ox, this);
            this.model.on('change:frame_yk', this.get_frame_ox, this);
            this.model.on('change:frame_zi', this.get_frame_ox, this);
            this.model.on('change:frame_zj', this.get_frame_ox, this);
            this.model.on('change:frame_zk', this.get_frame_ox, this);

            // Atom, UnitAtom, ...
            this.get_atom_x();
            this.get_atom_y();
            this.get_atom_z();
            this.get_atom_radii_dict();
            this.get_atom_colors_dict();
            this.get_atom_symbols();
            this.model.on('change:atom_x', this.get_x, this);
            this.model.on('change:atom_y', this.get_y, this);
            this.model.on('change:atom_z', this.get_z, this);
            this.model.on('change:atom_radii', this.get_atom_radii_dict, this);
            this.model.on('change:atom_colors', this.get_atom_colors_dict, this);
            this.model.on('change:atom_symbols', this.get_atom_symbols, this);

            // Two, PeriodicTwo
            this.get_two_bond0();
            this.get_two_bond1();
            this.model.on('change:two_bond0', this.get_two_bond0, this);
            this.model.on('change:two_bond1', this.get_two_bond1, this);

            //UField3D
            this.get_ufield3d_ox();
            this.get_ufield3d_oy();
            this.get_ufield3d_oz();
            this.get_ufield3d_nx();
            this.get_ufield3d_ny();
            this.get_ufield3d_nz();
            this.get_ufield3d_xi();
            this.get_ufield3d_xj();
            this.get_ufield3d_xk();
            this.get_ufield3d_yi();
            this.get_ufield3d_yj();
            this.get_ufield3d_yk();
            this.get_ufield3d_zi();
            this.get_ufield3d_zj();
            this.get_ufield3d_zk();
            this.model.on('change:ufield3d_ox', this.get_ufield3d_ox, this);
            this.model.on('change:ufield3d_oy', this.get_ufield3d_ox, this);
            this.model.on('change:ufield3d_oz', this.get_ufield3d_ox, this);
            this.model.on('change:ufield3d_nx', this.get_ufield3d_ox, this);
            this.model.on('change:ufield3d_ny', this.get_ufield3d_ox, this);
            this.model.on('change:ufield3d_nz', this.get_ufield3d_ox, this);
            this.model.on('change:ufield3d_xi', this.get_ufield3d_ox, this);
            this.model.on('change:ufield3d_xj', this.get_ufield3d_ox, this);
            this.model.on('change:ufield3d_xk', this.get_ufield3d_ox, this);
            this.model.on('change:ufield3d_yi', this.get_ufield3d_ox, this);
            this.model.on('change:ufield3d_yj', this.get_ufield3d_ox, this);
            this.model.on('change:ufield3d_yk', this.get_ufield3d_ox, this);
            this.model.on('change:ufield3d_zi', this.get_ufield3d_ox, this);
            this.model.on('change:ufield3d_zj', this.get_ufield3d_ox, this);
            this.model.on('change:ufield3d_zk', this.get_ufield3d_ox, this);
        };

        get_atom_x() {
            this.atom_x = this.get_trait('atom_x');
        };

        get_atom_y() {
            this.atom_y = this.get_trait('atom_y');
        };

        get_atom_z() {
            this.atom_z = this.get_trait('atom_z');
        };

        get_framelist() {
            this.framelist = this.get_trait('frame_frame');
        };

        get_atom_symbols() {
            this.atom_symbols = this.get_trait('atom_symbols');
        };

        get_atom_radii_dict() {
            this.atom_radii_dict = this.get_trait('atom_radii');
        };

        get_atom_colors_dict() {
            this.atom_colors_dict = this.get_trait('atom_colors');
        };

        get_two_bond0() {
            this.two_bond0 = this.get_trait('two_bond0');
        };

        get_two_bond1() {
            this.two_bond1 = this.get_trait('two_bond1');
        };

        get_frame_ox() {
            this.frame_ox = this.get_trait('frame_ox');
        };
        get_frame_oy() {
            this.frame_oy = this.get_trait('frame_oy');
        };
        get_frame_oz() {
            this.frame_oz = this.get_trait('frame_oz');
        };
        get_frame_xi() {
            this.frame_xi = this.get_trait('frame_xi');
        };
        get_frame_xj() {
            this.frame_xj = this.get_trait('frame_xj');
        };
        get_frame_xk() {
            this.frame_xk = this.get_trait('frame_xk');
        };
        get_frame_yi() {
            this.frame_yi = this.get_trait('frame_yi');
        };
        get_frame_yj() {
            this.frame_yj = this.get_trait('frame_yj');
        };
        get_frame_yk() {
            this.frame_yk = this.get_trait('frame_yk');
        };
        get_frame_zi() {
            this.frame_zi = this.get_trait('frame_zi');
        };
        get_frame_zj() {
            this.frame_zj = this.get_trait('frame_zj');
        };
        get_frame_zk() {
            this.frame_zk = this.get_trait('frame_zk');
        };

        get_ufield3d_ox() {
            this.ufield3d_ox = this.get_trait('ufield3d_ox');
        };
        get_ufield3d_oy() {
            this.ufield3d_oy = this.get_trait('ufield3d_oy');
        };
        get_ufield3d_oz() {
            this.ufield3d_oz = this.get_trait('ufield3d_oz');
        };
        get_ufield3d_nx() {
            this.ufield3d_nx = this.get_trait('ufield3d_nx');
        };
        get_ufield3d_ny() {
            this.ufield3d_ny = this.get_trait('ufield3d_ny');
        };
        get_ufield3d_nz() {
            this.ufield3d_nz = this.get_trait('ufield3d_nz');
        };
        get_ufield3d_xi() {
            this.ufield3d_xi = this.get_trait('ufield3d_xi');
        };
        get_ufield3d_xj() {
            this.ufield3d_xj = this.get_trait('ufield3d_xj');
        };
        get_ufield3d_xk() {
            this.ufield3d_xk = this.get_trait('ufield3d_xk');
        };
        get_ufield3d_yi() {
            this.ufield3d_yi = this.get_trait('ufield3d_yi');
        };
        get_ufield3d_yj() {
            this.ufield3d_yj = this.get_trait('ufield3d_yj');
        };
        get_ufield3d_yk() {
            this.ufield3d_yk = this.get_trait('ufield3d_yk');
        };
        get_ufield3d_zi() {
            this.ufield3d_zi = this.get_trait('ufield3d_zi');
        };
        get_ufield3d_zj() {
            this.ufield3d_zj = this.get_trait('ufield3d_zj');
        };
        get_ufield3d_zk() {
            this.ufield3d_zk = this.get_trait('ufield3d_zk');
        };
    };

    return {UniverseView: UniverseView};
});