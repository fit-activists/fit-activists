module.exports = function (grunt) {
    grunt.initConfig({
        less: {
            development: {
                options: {
                    // compress: true,
                    // yuicompress: true,
                    // optimization: 2
                },
                files: {
                    // target.css file: source.less file
                    "static/css/main.css": "less/main.less"
                }
            }
        },
        watch: {
            styles: {
                // Which files to watch (all .less files recursively in the less directory)
                files: ['less/**/*.less'],
                tasks: ['less'],
                options: {
                    spawn: false
                }
            }
        }
    });

    grunt.loadNpmTasks('grunt-contrib-less');
    grunt.loadNpmTasks('grunt-contrib-watch');
    grunt.loadNpmTasks('grunt-notify');

    grunt.registerTask('default', ['watch']);
};